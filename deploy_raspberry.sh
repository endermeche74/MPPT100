#!/bin/bash
# Script d'installation SolarWatch sur Raspberry Pi
# Lancer sur la Raspberry : bash deploy_raspberry.sh

set -e

APP_DIR="/home/soren/solarwatch"

echo "==> Création du dossier $APP_DIR"
mkdir -p "$APP_DIR"

echo "==> Copie des fichiers"
cp server.py index.html requirements.txt "$APP_DIR/"

echo "==> Création de l'environnement virtuel"
python3 -m venv "$APP_DIR/venv"

echo "==> Installation des dépendances"
"$APP_DIR/venv/bin/pip" install --upgrade pip -q
"$APP_DIR/venv/bin/pip" install -r "$APP_DIR/requirements.txt" -q

echo "==> Installation du service systemd"
sudo cp solarwatch.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable solarwatch
sudo systemctl restart solarwatch

echo ""
echo "==> Terminé !"
echo "    Serveur accessible sur : http://$(hostname -I | awk '{print $1}'):5000"
echo "    Statut : sudo systemctl status solarwatch"
echo "    Logs   : journalctl -u solarwatch -f"
