#!/bin/bash

PACKAGELOCK_FILE="package.lock"

if [ ! -f "$PACKAGELOCK_FILE" ]; then
    echo "Dependencies not installed."
    echo "Installing dependencies..."
    python3.10 -m pip install -r requirements.txt
    touch "$PACKAGELOCK_FILE"
fi

echo "Starting face recognition application."
python3.10 app-gui.py
