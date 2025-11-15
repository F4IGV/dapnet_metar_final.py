#!/usr/bin/env python3
"""
F4IGV et son amis Chat GPT presentent
metar_to_dapnet.py
Récupère le METAR de l'aéroport de selectionner et envoie un message via DAPNET.
"""

import requests
import json
from dateutil import parser as dateparser

# --- CONFIGURATION DAPNET ---
DAPNET_USER = "F4abc"
DAPNET_PASS = "123456"                 # ton mot de passe dapnet ici
CALLSIGN = ["f4abc", "f4def"]          # ton indicatif DAPNET enregistré
TX_GROUP = "f-53"                      # groupe de relais DAPNET (ex: fr-all, dl-all, hb9-all)

DAPNET_URL = "https://hampager.de/api/calls"

# --- CONFIG METAR ---
ICAO = "LFRN"  # Code OACI de l'aéroport choisis ( ici celui de rennes)
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
    """
    Construit un message POCSAG court depuis un METAR.
    Exemple : 'LFRN 131930Z 24008KT 9999 BKN030 11/08 Q1022'
    """
    if not metar_data:
        return None
    metar = metar_data["metar"]
    timestamp = metar_data["timestamp"]
    # on retire les éléments superflus si trop long (>80)
    msg = metar.strip()
    if len(msg) > 80:
        msg = msg[:80]
    return msg


def send_dapnet_message(message):
    """Envoie un message POCSAG via l’API DAPNET officielle."""
    payload = {
        "text": message,
        "callSignNames": [CALLSIGN],
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
        print(f"[OK] Message envoyé ({r.status_code}) : {message}")
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
    ok = send_dapnet_message(message)
    if ok:
        print("[SUCCÈS] Message METAR transmis à DAPNET.")
    else:
        print("[ÉCHEC] Envoi DAPNET échoué.")


if __name__ == "__main__":
    main()

