import subprocess
import sys
import time

def run_script(script_name):
    print(f"🚀 Running {script_name}...")
    try:
        # runs the python script and waits for it to finish
        result = subprocess.run([sys.executable, script_name], check=True)
        if result.returncode == 0:
            print(f"✅ {script_name} completed successfully.\n")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error while running {script_name}: {e}")
        sys.exit(1)

def main():
    print("--- NIGERIA HEALTH DASHBOARD: ETL PIPELINE ---")
    
    run_script("ingest_bronze.py")   # Get Raw
    run_script("process_silver.py") # Clean Data
    run_script("process_gold.py")   # Create Insights
    
    print("🎉 ETL Pipeline Complete! Starting Dashboard...")

    
    print("🌍 Launching Streamlit at http://localhost:8501")
    subprocess.run(["streamlit", "run", "app.py"])

if __name__ == "__main__":
    main()