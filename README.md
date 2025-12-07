# METAR to DAPNET Multi Sender  
By F4IGV and ChatGPT  
ASCII only - POCSAG compatible

This Python script retrieves the latest METAR report from a selected airport (default: LFRN Rennes) and sends it as a short ASCII message through the DAPNET pager network to multiple registered callsigns.

The script is simple, fast, lightweight, and ideal for amateur radio operators who want aviation weather updates on their POCSAG pagers.

This script can be automated on Windows using Task Scheduler together with the `.bat` file included in this repository.  
The user must edit the `.bat` file and specify the full path to the `.py` script so automation works correctly.

---

## Features

- Retrieves the latest METAR from NOAA servers  
- Supports any ICAO airport code  
- Sends METAR as a POCSAG message to multiple DAPNET callsigns  
- Supports transmitter groups  
- Fully ASCII (POCSAG safe)  
- Automatic trimming to 80 chars max  
- Simple configuration section  

---

## Message example

```text
LFRN 121430Z 23010KT 9999 FEW025 SCT040 11/06 Q1013
```

If the message is longer than 80 characters, it is truncated automatically.

---

## Installation

### 1. Clone the repository
```bash
git clone https://github.com/your_username/your_repository.git
cd your_repository
```

### 2. Install Python 3
Python 3.8 or newer is recommended.

Check your version:
```bash
python --version
```

### 3. Install required packages
```bash
pip install requests python-dateutil
```

---

## Configuration

Edit the script and set your DAPNET access:

```python
DAPNET_USER = "f4abc"
DAPNET_PASS = "123456"
CALLSIGNS = ["f4abc", "f5def"]
TX_GROUP   = "f-53"
```

Configure the airport ICAO (default: LFRN - Rennes):

```python
ICAO = "LFRN"
```

NOAA METAR source:
```python
METAR_URL = f"https://tgftp.nws.noaa.gov/data/observations/metar/stations/{ICAO}.TXT"
```

---

## Manual execution

```bash
python metar_to_dapnet_multi.py
```

Example output:
```text
Recuperation du METAR pour LFRN...
Donnees METAR : {'timestamp': '2025/01/12 14:30', 'metar': 'LFRN 121430Z 23010KT 9999 FEW025 SCT040 11/06 Q1013'}
Message POCSAG : LFRN 121430Z 23010KT 9999 FEW025 SCT040 11/06 Q1013
[OK] Message envoye a f4abc, f5def : LFRN 121430Z 23010KT...
[SUCCES] Message METAR transmis a tous les CALLSIGN.
```

---

## How it works

1. Script retrieves raw METAR text from NOAA  
2. Extracts timestamp + METAR line  
3. Builds an ASCII safe message (max 80 chars)  
4. Sends the message via the DAPNET API to all selected callsigns  
5. Displays result and errors if present  

No state files, logs, or external dependencies beyond Python packages.

---

## Project structure

```
metar_to_dapnet_multi.py   # Main script
README.md                  # Documentation
```

---

## Requirements

- Python 3.8+  
- requests  
- python-dateutil  

Install all dependencies:
```bash
pip install requests python-dateutil
```

---

## Troubleshooting

- METAR not retrieved  
  - NOAA may be temporarily unavailable  
  - Check ICAO code  

- DAPNET error  
  - Check your DAPNET user, password, or membership  
  - Verify TX group permissions  

- Message not sent  
  - Ensure callsigns are registered in DAPNET  
  - Check network connectivity  

---

## License

This project is released for amateur radio experimentation only.  
Use at your own responsibility.

---

## Credits

Developed by **F4IGV** with assistance from **ChatGPT**.  
Thanks to the amateur radio community for feedback and tests.



exemple de log généré:


<img width="1187" height="616" alt="screen_log_metar" src="https://github.com/user-attachments/assets/1e5f9496-820b-4a19-a32a-dfdd6ce2ceb8" />
