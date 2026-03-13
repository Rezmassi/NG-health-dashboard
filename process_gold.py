import pandas as pd
import os

def create_gold_layer():
    print("Transforming Silver to Gold...")
    
    # 1. Load Silver Data
    df_trends = pd.read_csv("data/02_silver/national_health_trends.csv")
    
    # 2. CREATE GOLD INSIGHT 1: Growth Rates
    #the Year-over-Year change calculated so the dashboard can show "Progress"
    df_trends['YoY_Change'] = df_trends['Stunting_Rate'].diff()
    gold_trends = df_trends[['Year', 'Stunting_Rate', 'YoY_Change']]
    
    # 3. CREATE GOLD INSIGHT 2: Regional Risk Profile
    # (Assuming therw's state-level data in Silver)
    # We could rank states by 'High', 'Medium', or 'Low' risk
    
    # Ensure directory exists
    os.makedirs("data/03_gold", exist_ok=True)
    
    # 4. Save to Gold
    gold_trends.to_csv("data/03_gold/stunting_analytics.csv", index=False)
    print("✅ Gold Layer updated: data/03_gold/stunting_analytics.csv")

if __name__ == "__main__":
    create_gold_layer()