import pandas as pd
import os
import knoema

print("Script is starting using Knoema library...")

def fetch_health_data():
    try:
        # jgngifg is the dataset ID
        print("Accessing Knoema dataset: jgngifg")

        # This returns a multi-index DataFrame
        df = knoema.get('jgngifg')

        # Flatten multi-index if necessary
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = ['_'.join(map(str, col)).strip() for col in df.columns.values]

        df = df.reset_index()

        return df

    except Exception as e:
        print(f"Knoema access failed: {e}")
        return None


def save_to_bronze():
    print("Fetching data via Knoema API...")

    df = fetch_health_data()

    if df is None:
        print("Fetch failed, so nothing to save.")
        return

    os.makedirs("data/01_bronze", exist_ok=True)

    path = "data/01_bronze/health_data_raw.csv"

    df.to_csv(path, index=False)

    print(f"Done! Saved {len(df)} records.")


if __name__ == "__main__":
    save_to_bronze()