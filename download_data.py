# download_data.py
import os
import requests
from asset_registry import ASSETS

BASE_URL = "https://highspell.com:8887/static/"
DEFAULT_EXTENSION = ".carbon"
OUTPUT_DIR = "game_asset_files"

def download_file(name, meta, output_dir=OUTPUT_DIR):
    file_name = meta.get("filename") or f"{name}.{meta['version']}{DEFAULT_EXTENSION}"
    url = f"{BASE_URL}{meta['subpath']}{file_name}"
    local_path = os.path.join(output_dir, meta["subpath"], file_name)

    try:
        response = requests.get(url)
        response.raise_for_status()
        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        with open(local_path, 'wb') as f:
            f.write(response.content)
        print(f"✅ Downloaded {file_name}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to download {file_name}: {e}")

if __name__ == "__main__":
    for asset_name, metadata in ASSETS.items():
        if "filename" in metadata or isinstance(metadata.get("version"), (int, float)):
            download_file(asset_name, metadata)
        else:
            print(f"⚠️ Skipping {asset_name}: missing valid filename or version")
    print("All downloads completed.")