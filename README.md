# 🇳🇬 Nigeria Health Explorer: Data Pipeline & Dashboard

An end-to-end Data Engineering project that visualizes critical public health metrics (Malaria and Malnutrition) across Nigeria. This project utilizes a **Medallion Architecture** to transform raw health data into actionable insights.

---

## 🏗️ The Architecture (Medallion Folders)
This project follows professional data engineering standards by separating data into three distinct layers:

1.  **🟫 Bronze (Raw):** Untouched data ingested directly from source APIs or CSVs.
2.  **🥈 Silver (Cleaned):** Data that has been standardized, missing values handled, and state names normalized.
3.  **🥇 Gold (Analytics):** High-value, aggregated tables (e.g., Year-over-Year stunting growth) ready for visualization.




## 🛠️ Features
* **Malaria Tracking:** Interactive geographic map showing prevalence across Nigerian states.
* **Malnutrition Trends:** Historical analysis (1990–2021) of stunting rates with "Data Lag" transparency.
* **Regional Filtering:** Ability to filter data by Geopolitical Zones (North West, South West, etc.).
* **Automated Pipeline:** A master script that runs the entire ETL process in sequence.

---

## 🚀 Getting Started

### 1. Prerequisites
Ensure you have **Python 3.9+** installed on your computer.

### 2. Installation
Clone this repository and navigate into the folder:
```bash
git clone [https://github.com/Rezmassi/NG-health-dashboard.git](https://github.com/Rezmassi/NG-health-dashboard.git)
cd NG-health-dashboard
```

### 3. Install Requirements
Install the necessary libraries using the provided requirements file:

```bash
pip install -r requirements.txt
```

### 4. Run the Full Pipeline
You don't need to run scripts individually. Simply run the Orchestrator:

```bash
python run_all.py
```

This will:

- Ingest Raw Data (Bronze)

- Clean the Data (Silver)

- Generate Insights (Gold)

- Launch the Streamlit Dashboard in your browser.

  ---

## 👨‍💻  Developer
Ridwan Badamasi

---

## 📊  Data Sources
Demographic and Health Surveys (DHS)

Multiple Indicator Cluster Surveys (MICS)

World Bank Open Data
