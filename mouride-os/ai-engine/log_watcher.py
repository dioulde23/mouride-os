import time

def check_logs(log_file):
    try:
        with open(log_file, 'r') as f:
            for line in f:
                if "error" in line.lower():
                    print("[ALERT] Error detected :", line.strip())
    except FileNotFoundError:
        print("🚫 Fichier de log non trouvé :", log_file)

if __name__ == "__main__":
    while True:
        check_logs("logs/system.log")
        time.sleep(10)
