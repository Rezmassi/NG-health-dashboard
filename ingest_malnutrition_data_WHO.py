import requests
import pandas as pd
import os

def fetch_world_bank_data():
    # Indicator: Prevalence of stunting, height for age (% of children under 5)
    # Country: Nigeria (NG)
    url = "https://api.worldbank.org/v2/country/NG/indicator/SH.STA.STNT.ZS?format=json"
    
    print("Connecting to World Bank API...")
    try:
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            data = response.json()
            # World Bank JSON: [metadata, actual_data]
            actual_data = data[1]
            
            rows = []
            for record in actual_data:
                # We only want entries where there is a real value
                if record['value'] is not None:
                    rows.append({
                        "Country": record['country']['value'],
                        "Year": record['date'],
                        "Stunting_Rate": record['value']
                    })
            return pd.DataFrame(rows)
        else:
            print(f"World Bank Error: {response.status_code}")
            return None
    except Exception as e:
        print(f"Connection failed: {e}")
        return None

def save_to_bronze():
    df = fetch_world_bank_data()
    if df is not None:
        os.makedirs("data/01_bronze", exist_ok=True)
        path = "data/01_bronze/malnutrition_raw.csv"
        df.to_csv(path, index=False)
        print(f"Success! Retrieved {len(df)} years of Nigerian stunting data.")
    else:
        print("Failed to fetch World Bank data.")

if __name__ == "__main__":
    save_to_bronze()