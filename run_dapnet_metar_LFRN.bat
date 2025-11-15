@echo off
REM Lance le script Python pour envoyer la météo solaire sur DAPNET
cd /d "C:\Scripts\DAPNET"
py "dapnet_metar_LFRN.py" >> "C:\Scripts\DAPNET\dapnet_metar_LFRN.log" 2>&1