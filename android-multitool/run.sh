#!/usr/bin/env bash
set -e

echo "============================================"
echo "  Android Multitool - launcher"
echo "============================================"

if ! command -v python3 >/dev/null 2>&1; then
    echo "[!] python3 was not found. Install it from https://www.python.org/downloads/"
    exit 1
fi

echo "[*] Checking dependencies..."
python3 -m pip install -r requirements.txt --quiet --disable-pip-version-check

echo "[*] Starting Android Multitool..."
python3 src/main.py
