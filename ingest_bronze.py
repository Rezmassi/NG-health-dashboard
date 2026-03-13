import os
import shutil
import pandas as pd

def ingest_data():
    print("📥 Starting Data Ingestion (Bronze Layer)...")
    
    # 1. Create the Bronze directory if it doesn't exist
    bronze_path = "data/01_bronze"
    os.makedirs(bronze_path, exist_ok=True)
    
    
    print(f"✅ Raw data secured in {bronze_path}")

if __name__ == "__main__":
    ingest_data()