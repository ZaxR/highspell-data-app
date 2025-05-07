import os
import requests


BASE_URL = "https://highspell.com:8887/static/"
DEFAULT_EXTENSION = ".carbon"
OUTPUT_DIR = "game_asset_files"

"""
Unified dictionary of all game asset files
Found via:
1. Opening https://highspell.com/game
2. Opening Developer > Developer Tools (Networking Tab)
3. Logging in to the game
4. Viewing the "assetsClient" request
"""
game_asset_files = {
    # .carbon files
    "itemdefs": {"version": 25, "subpath": ""},
    "worldentitydefs": {"version": 10, "subpath": ""},
    "worldentities": {"version": 20, "subpath": ""},
    "npcentitydefs": {"version": 18, "subpath": ""},
    "npcentities": {"version": 17, "subpath": ""},
    "instancednpcentities": {"version": 5, "subpath": ""},
    "shopdefs": {"version": 9, "subpath": ""},
    "conversationdefs": {"version": 7, "subpath": ""},
    "grounditems": {"version": 12, "subpath": ""},
    "spelldefs": {"version": 7, "subpath": ""},
    "npcloot": {"version": 13, "subpath": ""},
    "questdefs": {"version": 3, "subpath": ""},
    "pickpocketdefs": {"version": 2, "subpath": ""},
    "worldentitylootdefs": {"version": 6, "subpath": ""},
    "npcconversationdefs": {"version": 2, "subpath": ""},
    "worldentityactions": {"version": 4, "subpath": ""},
    "specialcoordinatesdefs": {"version": 1, "subpath": ""},
    "appearance": {"version": 36, "subpath": "carbon/"},
    "creatures": {"version": 17, "subpath": "carbon/"},
    "heightmaps": {"version": 23, "subpath": "carbon/"},
    "items": {"version": 43, "subpath": "carbon/"},
    "meshes": {"version": 43, "subpath": "carbon/"},
    "textures": {"version": 31, "subpath": "carbon/"},

    # Additional asset files (non-carbon, no version)
    "earthoverworldtexture": {"subpath": "assets/heightmaps/", "filename": "earthoverworldtexture.png"},
    "earthoverworldmap": {"subpath": "assets/heightmaps/", "filename": "earthoverworldmap.png"},
    "earthoverworldpath": {"subpath": "assets/heightmaps/", "filename": "earthoverworldpath.png"},
    "earthskytexture": {"subpath": "assets/heightmaps/", "filename": "earthskytexture.png"},
    "earthskymap": {"subpath": "assets/heightmaps/", "filename": "earthskymap.png"},
    "earthskypath": {"subpath": "assets/heightmaps/", "filename": "earthskypath.png"},
    "earthundergroundtexture": {"subpath": "assets/heightmaps/", "filename": "earthundergroundtexture.png"},
    "earthundergroundmap": {"subpath": "assets/heightmaps/", "filename": "earthundergroundmap.png"},
    "earthundergroundpath": {"subpath": "assets/heightmaps/", "filename": "earthundergroundpath.png"},
    "moontexture": {"subpath": "assets/heightmaps/", "filename": "moontexture.png"},
    "moonmap": {"subpath": "assets/heightmaps/", "filename": "moonmap.png"},
    "moonpath": {"subpath": "assets/heightmaps/", "filename": "moonpath.png"},
}

# Download function
def download_file(name, meta, output_dir=OUTPUT_DIR):
    # Determine full filename and URL
    file_name = meta["filename"] if "filename" in meta else f"{name}.{meta['version']}{DEFAULT_EXTENSION}"
    
    url = f"{BASE_URL}{meta['subpath']}{filename}"
    local_path = os.path.join(output_dir, meta["subpath"], filename)

    try:
        response = requests.get(url)
        response.raise_for_status()
        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        with open(local_path, 'wb') as f:
            f.write(response.content)
        print(f"✅ Downloaded {filename}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to download {filename}: {e}")

# Download all files
for asset_name, metadata in game_asset_files.items():
    if "version" in metadata:
        # Check if the version is a number
        if not isinstance(metadata["version"], (int, float)):
            print(f"❌ Invalid version for {asset_name}: {metadata['version']}")
            continue

        download_file(asset_name, metadata)
