import requests
import pandas as pd
import io
import os

print("Starting Full-Country Malaria Ingestion...")

def fetch_hdx_malaria_data():
    # This is the direct HDX download link for Nigeria Sub-national Malaria Indicators
    url = "https://data.humdata.org/dataset/6de94d23-f178-458d-ad0b-69a75d9e0b00/resource/77b90879-c905-4d82-bda5-05d32a628312/download/malaria-parasitemia_subnational_nga.csv"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    try:
        response = requests.get(url, headers=headers, timeout=20)
        if response.status_code == 200:
            # Load the CSV data directly from the response
            df = pd.read_csv(io.StringIO(response.text))
            
            # Cleaning the HDX/DHS format
            # CharacteristicLabel usually contains the State names
            # Value contains the percentage
            if 'CharacteristicLabel' in df.columns:
                df = df.rename(columns={
                    'CharacteristicLabel': 'State',
                    'Value': 'Malaria_Prevalence'
                })
                # filter for only the most recent survey rows if needed
                return df[['State', 'Malaria_Prevalence']]
            return df
        else:
            print(f"HDX Error: {response.status_code}")
            return None
    except Exception as e:
        print(f"Connection failed: {e}")
        return None

def save_to_bronze():
    df = fetch_hdx_malaria_data()
    if df is not None:
        os.makedirs("data/01_bronze", exist_ok=True)
        path = "data/01_bronze/malaria_full_country.csv"
        df.to_csv(path, index=False)
        print(f"Success! Saved data for {len(df)} entries (States + National).")
    else:
        print("Pipeline failed to retrieve HDX data.")

if __name__ == "__main__":
    save_to_bronze()