#!/usr/bin/env python3
"""
metar_to_dapnet_multi.py
Récupère le METAR de l'aéroport de Rennes (LFRN) et envoie un message via DAPNET à plusieurs CALLSIGN.
"""

import requests
import json
from dateutil import parser as dateparser

# --- CONFIGURATION DAPNET ---
DAPNET_USER = "f4abc"
DAPNET_PASS = "123456"             # your password for dapnet
CALLSIGNS = ["f4abc", "f5def"]  # Liste de CALLSIGN DAPNET enregistrés
TX_GROUP = "f-53"  # groupe de relais DAPNET (ex: fr-all, dl-all, hb9-all)

DAPNET_URL = "https://hampager.de/api/calls"

# --- CONFIG METAR ---
ICAO = "LFRN"  # Rennes
METAR_URL = f"https://tgftp.nws.noaa.gov/data/observations/metar/stations/{ICAO}.TXT"


def fetch_metar(icao=ICAO):
    """Récupère le dernier METAR brut depuis NOAA."""
    try:
        r = requests.get(METAR_URL, timeout=10)
        r.raise_for_status()
        lines = r.text.strip().splitlines()
        if len(lines) < 2:
            raise ValueError("METAR non trouvé ou vide")
        timestamp = lines[0]
        metar = lines[1]
        return {"timestamp": timestamp, "metar": metar}
    except Exception as e:
        print(f"[ERREUR] Récupération METAR : {e}")
        return None


def build_metar_message(metar_data):
    """Construit un message POCSAG court depuis un METAR."""
    if not metar_data:
        return None
    metar = metar_data["metar"]
    timestamp = metar_data["timestamp"]
    msg = metar.strip()
    if len(msg) > 80:
        msg = msg[:80]
    return msg


def send_dapnet_message(message, callsigns):
    """
    Envoie un message POCSAG via l’API DAPNET à plusieurs CALLSIGN.
    """
    payload = {
        "text": message,
        "callSignNames": callsigns,
        "transmitterGroupNames": [TX_GROUP],
        "emergency": False
    }

    headers = {"Content-Type": "application/json"}

    try:
        r = requests.post(
            DAPNET_URL,
            auth=(DAPNET_USER, DAPNET_PASS),
            headers=headers,
            data=json.dumps(payload),
            timeout=10
        )
        r.raise_for_status()
        print(f"[OK] Message envoyé à {', '.join(callsigns)} ({r.status_code}) : {message}")
        return True
    except requests.HTTPError as he:
        print(f"[ERREUR HTTP] {he} / {getattr(he.response, 'text', None)}")
    except Exception as e:
        print(f"[ERREUR PYTHON] {e}")
    return False


def main():
    print(f"Récupération du METAR pour {ICAO}...")
    metar_data = fetch_metar()
    if not metar_data:
        print("[ÉCHEC] Impossible de récupérer le METAR.")
        return

    print("Données METAR :", metar_data)
    message = build_metar_message(metar_data)
    if not message:
        print("[ÉCHEC] Message METAR vide.")
        return

    print("Message POCSAG :", message)
    ok = send_dapnet_message(message, CALLSIGNS)
    if ok:
        print("[SUCCÈS] Message METAR transmis à tous les CALLSIGN.")
    else:
        print("[ÉCHEC] Envoi DAPNET échoué.")


if __name__ == "__main__":
    main()
