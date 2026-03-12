import pandas as pd
import json
import os

def process_silver_layer():
    print("Starting Silver Layer Processing...")
    os.makedirs("data/02_silver", exist_ok=True)

    # --- PART 1: STATE-LEVEL DATA (For the Map) ---
    # Coordinates for all 36 states + FCT
    state_coords = {
        "Abia": [5.45, 7.52], "Adamawa": [9.32, 12.44], "Akwa Ibom": [5.01, 7.91],
        "Anambra": [6.21, 7.06], "Bauchi": [10.31, 9.84], "Bayelsa": [4.77, 6.06],
        "Benue": [7.33, 8.53], "Borno": [11.83, 13.15], "Cross River": [5.96, 8.33],
        "Delta": [5.70, 5.89], "Ebonyi": [6.26, 8.05], "Edo": [6.33, 5.62],
        "Ekiti": [7.63, 5.22], "Enugu": [6.45, 7.50], "FCT Abuja": [9.07, 7.40],
        "Gombe": [10.28, 11.16], "Imo": [5.48, 7.03], "Jigawa": [12.00, 9.33],
        "Kaduna": [10.52, 7.43], "Kano": [12.00, 8.51], "Katsina": [12.98, 7.60],
        "Kebbi": [11.50, 4.00], "Kogi": [7.73, 6.67], "Kwara": [8.50, 4.55],
        "Lagos": [6.52, 3.37], "Nasarawa": [8.50, 7.70], "Niger": [9.08, 6.55],
        "Ogun": [7.16, 3.35], "Ondo": [7.25, 5.20], "Osun": [7.56, 4.56],
        "Oyo": [7.38, 3.93], "Plateau": [9.21, 9.51], "Rivers": [4.75, 7.00],
        "Sokoto": [13.06, 5.24], "Taraba": [8.00, 10.50], "Yobe": [12.00, 11.50],
        "Zamfara": [12.12, 6.66]
    }

    try:
        df_malaria_states = pd.read_csv("data/01_bronze/malaria_full_country.csv")
        
        features = []
        for state, point in state_coords.items():
            match = df_malaria_states[df_malaria_states['State'].str.contains(state, case=False, na=False)]
            val = float(match.iloc[0]['Malaria_Prevalence']) if not match.empty else 0.0

            features.append({
                "type": "Feature",
                "properties": {"state": state, "Malaria_Prevalence": val},
                "geometry": {"type": "Point", "coordinates": [point[1], point[0]]}
            })

        with open("data/02_silver/health_map_combined.json", "w") as f:
            json.dump({"type": "FeatureCollection", "features": features}, f)
        print("✅ State-level GeoJSON created.")
    except Exception as e:
        print(f"❌ Error processing state data: {e}")


    # --- PART 2: NATIONAL TRENDS (The block you asked about) ---
    try:
        # Load the national files you created in your ingestion scripts
        malaria_national = pd.read_csv("data/01_bronze/malaria_raw.csv")
        malnutrition_national = pd.read_csv("data/01_bronze/malnutrition_raw.csv")

        # Combine the two national files
        trends = pd.merge(malaria_national, malnutrition_national, on="Year", how="outer")

        # RENAME columns so the Dashboard knows exactly what they are
        trends = trends.rename(columns={
            "Value_x": "Malaria_National",
            "Value_y": "Stunting_National"
        })

        # Save to Silver
        trends.to_csv("data/02_silver/national_health_trends.csv", index=False)
        print("✅ National trends CSV created with renamed columns.")
        
    except Exception as e:
        print(f"❌ Error processing trends: {e}")

if __name__ == "__main__":
    process_silver_layer()