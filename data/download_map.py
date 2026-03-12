import requests
import os

def download_nigeria_geojson():
    # Mirroring the GeoBoundaries ADM1 (States) from HDX
    url = "https://data.humdata.org/dataset/geoboundaries-admin-boundaries-for-nigeria/resource/3a198c00-bb58-45e2-b6ce-ca625eb0246a/download/geoboundaries-nga-adm1_simplified.geojson"
    
    # Adding a User-Agent is critical to bypass simple server blocks
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    path = "data/01_bronze/nigerian_states.json"
    os.makedirs("data/01_bronze", exist_ok=True)

    print("Downloading official Nigerian state boundaries (HDX Mirror)...")
    try:
        # Increased timeout to 60 seconds to handle larger geographic files
        response = requests.get(url, headers=headers, timeout=60)
        response.raise_for_status() # This will catch 404, 403, or 500 errors

        with open(path, "wb") as f:
            f.write(response.content)
            
        print(f"Success! Full map saved to {path}")
        print(f"File size: {os.path.getsize(path) / 1024:.2f} KB")

    except requests.exceptions.Timeout:
        print("Error: The connection timed out. Try checking your internet speed.")
    except Exception as e:
        print(f"Download failed: {e}")

if __name__ == "__main__":
    download_nigeria_geojson()