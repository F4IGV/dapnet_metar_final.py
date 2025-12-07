@echo off
REM Lance le script Python pour envoyer la météo solaire sur DAPNET
cd /d "C:\Scripts\DAPNET"  #choose your folder who contain the .py file

py "dapnet_metar_final.py" >> "C:\Scripts\DAPNET\dapnet_metar_final.log" 2>&1

