@echo off
echo Deploiement SolarWatch sur Raspberry Pi...

scp "%~dp0server.py" "%~dp0index.html" "%~dp0requirements.txt" soren@192.168.137.6:~/solarwatch/
ssh soren@192.168.137.6 "sudo systemctl restart solarwatch"

echo.
echo Deploiement termine ! Site accessible sur https://solarwatch-reunion.online
pause
