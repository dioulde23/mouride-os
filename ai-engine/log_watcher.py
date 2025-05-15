import time
import re
from pathlib import Path

# === CONFIGURATION ===
LOG_FILE_PATH = Path("logs/system.log")  # tu peux créer ce fichier toi-même pour tester
ERROR_KEYWORDS = ["error", "critical", "fail", "unauthorized", "crash"]

def detect_suspicious(line):
    """Analyse une ligne et détecte les comportements suspects"""
    for keyword in ERROR_KEYWORDS:
        if re.search(keyword, line, re.IGNORECASE):
            return True
    return False

def watch_log():
    print(f"📡 Surveillance du fichier : {LOG_FILE_PATH}")

    if not LOG_FILE_PATH.exists():
        print("🚫 Fichier de log introuvable.")
        return

    with LOG_FILE_PATH.open("r") as f:
        f.seek(0, 2)  # se positionner à la fin du fichier

        while True:
            line = f.readline()
            if not line:
                time.sleep(1)
                continue
            if detect_suspicious(line):
                print(f"🚨 Suspicious activity detected: {line.strip()}")
            else:
                print(f"✅ {line.strip()}")

if __name__ == "__main__":
    watch_log()

# ai-engine/log_watcher.py

import time
from log_analyzer import detect_anomalies

def watch_log_file(log_file_path):
    with open(log_file_path, 'r') as log_file:
        log_file.seek(0, 2)  # Aller à la fin du fichier
        while True:
            line = log_file.readline()
            if not line:
                time.sleep(1)
                continue

            anomalies = detect_anomalies([line])
            if anomalies:
                print("[⚠️ ALERTE] Anomalies détectées :", anomalies)

if __name__ == "__main__":
    log_path = "logs/system.log"
    watch_log_file(log_path)
