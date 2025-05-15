import os
import requests
import hashlib
import logging
from datetime import datetime
from tqdm import tqdm  # Pour une barre de progrès stylée
import math
import zipfile

class AutoUpdater:
    def __init__(self):
        # Remplacez 'ton_user' par votre nom d'utilisateur GitHub réel
        self.repo_url = "https://api.github.com/repos/ton_user/mouride-os/releases/latest"
        self.current_version = self.get_current_version()
        self.logger = self.setup_logger()

    def setup_logger(self):
        logging.basicConfig(
            filename='logs/system.log',
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        return logging.getLogger('AutoUpdater')

    def get_current_version(self):
        # Lire depuis un fichier version.txt à créer
        try:
            with open('version.txt', 'r') as f:
                return f.read().strip()
        except FileNotFoundError:
            return "0.1.0"  # Version par défaut

    def check_for_updates(self):
        try:
            response = requests.get(self.repo_url)
            if response.status_code != 200:
                self.logger.error(f"[{datetime.now()}] Failed to fetch release info: HTTP {response.status_code}")
                return None, None
            data = response.json()
            latest_version = data.get('tag_name')
            assets = data.get('assets', [])
            if latest_version != self.current_version:
                if not assets:
                    self.logger.warning(f"[{datetime.now()}] No assets found for the latest release {latest_version}")
                    return None, None
                self.logger.info(f"[{datetime.now()}] Update found: {latest_version}")
                return latest_version, assets[0].get('browser_download_url')
            return None, None
        except Exception as e:
            self.logger.error(f"[{datetime.now()}] Update check failed: {str(e)}")
            return None, None

    def download_update(self, url, dest_path="update.zip"):
        try:
            with requests.get(url, stream=True) as r:
                r.raise_for_status()
                total_size = int(r.headers.get('content-length', 0))
                chunk_size = 8192
                total_chunks = math.ceil(total_size / chunk_size) if total_size else None

                with open(dest_path, 'wb') as f:
                    for chunk in tqdm(r.iter_content(chunk_size=chunk_size), 
                                      total=total_chunks, 
                                      unit='KB', 
                                      unit_scale=True):
                        f.write(chunk)
                return True
        except Exception as e:
            self.logger.error(f"[{datetime.now()}] Download failed: {str(e)}")
            return False

    def apply_update(self, update_path):
        try:
            if not os.path.exists(update_path):
                self.logger.error(f"[{datetime.now()}] Update file {update_path} does not exist.")
                return False
            with zipfile.ZipFile(update_path, 'r') as zip_ref:
                zip_ref.extractall(".")
            # After extraction, update the version.txt file
            # Assuming the version is in the zip filename or passed somehow; here we just log
            self.logger.info(f"[{datetime.now()}] Update applied successfully from {update_path}")
            # Optionally, update the version.txt file here if new version info is available
            return True
        except Exception as e:
            self.logger.error(f"[{datetime.now()}] Failed to apply update: {str(e)}")
            return False

# Exemple d'utilisation
if __name__ == "__main__":
    updater = AutoUpdater()
    new_version, download_url = updater.check_for_updates()
    
    if new_version:
        print(f"Téléchargement de la version {new_version}...")
        if updater.download_update(download_url):
            if updater.apply_update("update.zip"):
                print("Mise à jour appliquée avec succès.")
            else:
                print("Échec de l'application de la mise à jour.")
        else:
            print("Échec du téléchargement de la mise à jour.")
    else:
        print("Aucune mise à jour disponible.")
