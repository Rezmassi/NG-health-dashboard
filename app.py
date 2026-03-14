import streamlit as st
import pandas as pd
import json
import folium
from streamlit_folium import st_folium, folium_static
import altair as alt

# 1. PAGE CONFIGURATION
st.set_page_config(page_title="Nigeria Health Dashboard", layout="wide")

# 2. DATA LOADING & REGIONAL MAPPING
@st.cache_data
def load_state_data():
    # Loading the Point-based JSON from Silver stage
    try:
        with open("data/02_silver/health_map_combined.json", "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        st.error("Missing GeoJSON file. Please run process_silver.py.")
        st.stop()
    
    # Mapping Nigerian States to Geopolitical Zones for the filter
    zones = {
        'North West': ['Kano', 'Kaduna', 'Katsina', 'Sokoto', 'Kebbi', 'Zamfara', 'Jigawa'],
        'North East': ['Bauchi', 'Borno', 'Yobe', 'Taraba', 'Adamawa', 'Gombe'],
        'North Central': ['Kwara', 'Kogi', 'Niger', 'Benue', 'Plateau', 'Nasarawa', 'FCT Abuja'],
        'South West': ['Lagos', 'Oyo', 'Ogun', 'Ondo', 'Osun', 'Ekiti'],
        'South South': ['Rivers', 'Delta', 'Edo', 'Akwa Ibom', 'Cross River', 'Bayelsa'],
        'South East': ['Abia', 'Anambra', 'Enugu', 'Imo', 'Ebonyi']
    }
    
    state_to_zone = {state: zone for zone, states in zones.items() for state in states}
    
    rows = []
    for feature in data['features']:
        row = feature['properties']
        lon, lat = feature['geometry']['coordinates']
        row['lon'], row['lat'] = float(lon), float(lat)
        row['Zone'] = state_to_zone.get(row['state'], 'Unknown')
        rows.append(row)
    return pd.DataFrame(rows)

@st.cache_data
def load_trend_data():
    try:
        return pd.read_csv("data/03_gold/stunting_analytics.csv")
    except FileNotFoundError:
        st.error("Missing Trends CSV file. Please run process_silver.py.")
        st.stop()

    

# Initialize Data
df_states = load_state_data()
df_trends = load_trend_data()

# 3. SIDEBAR NAVIGATION
st.sidebar.header("🇳🇬 Health Tracks")
view_option = st.sidebar.selectbox(
    "Choose Analysis Track:", 
    ["Malaria: Geographic Spread", "Malnutrition: Historical Trends"]
)

# --- SIDEBAR AUTHOR INFO ---
st.sidebar.markdown("---")
st.sidebar.markdown("### 👨‍💻 Developed by:")
st.sidebar.write("**Ridwan Badamasi**")
st.sidebar.markdown("[LinkedIn](https://www.linkedin.com/in/ridwan-badamasi) | [GitHub](https://github.com/Rezmassi)")


# 4. SHARED FILTERS (Sidebar)
st.sidebar.markdown("---")
st.sidebar.subheader("Filters")

# Multi-select for Zones
selected_zones = st.sidebar.multiselect(
    "Select Geopolitical Zones:",
    options=sorted(df_states['Zone'].unique()),
    default=sorted(df_states['Zone'].unique())
)

# Search Bar for specific States
search_query = st.sidebar.selectbox(
    "Search Specific State:",
    options=[""] + sorted(df_states['state'].tolist())
)

# Filtering Logic
df_filtered = df_states[df_states['Zone'].isin(selected_zones)].copy()
df_filtered['Malaria_Prevalence'] = pd.to_numeric(df_filtered['Malaria_Prevalence'], errors='coerce').fillna(0)

# 5. MAIN INTERFACE LOGIC

# --- TRACK 1: MALARIA (MAP) ---
if view_option == "Malaria: Geographic Spread":
    st.title("🦟 Malaria Tracking (State-Level)")
    
    # KPIs for filtered zones
    avg_prev = df_filtered['Malaria_Prevalence'].mean()
    if pd.isna(avg_prev):
        avg_prev = 0
    st.metric("Avg Prevalence in Selected Zones", f"{float(avg_prev):.1f}%")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Map Centering Logic
        if search_query:
            state_info = df_states[df_states['state'] == search_query].iloc[0]
            map_center = [state_info['lat'], state_info['lon']]
            zoom = 8
        else:
            map_center = [9.08, 8.67]
            zoom = 6
            
        # Create a dynamic key to force the map to refresh properly
        map_key = f"map_{len(df_filtered)}_{search_query}"

        m = folium.Map(location=map_center, zoom_start=zoom, tiles="CartoDB positron")
        
        for _, row in df_filtered.iterrows():
            # Ensure prevalence is a clean number
            prev = float(row.get('Malaria_Prevalence', 0))
            
            is_searched = (row['state'] == search_query)
            color = "#FFD700" if is_searched else "#D90429"
            
            # Use max() to ensure radius is NEVER 0 or NaN
            safe_radius = max(prev * 0.7, 1.0) if not is_searched else 20
            
            folium.CircleMarker(
                location=[row['lat'], row['lon']],
                radius=safe_radius,
                popup=f"State: {row['state']}<br>Prevalence: {prev}%",
                color=color,
                fill=True,
                fill_opacity=0.7
            ).add_to(m)
        
        # Call st_folium with the dynamic key
        st_folium(m, use_container_width=True, height=500)

    with col2:
        st.write("**Zone Breakdown**")
        st.dataframe(
            df_filtered[['state', 'Malaria_Prevalence']].sort_values(by="Malaria_Prevalence", ascending=False),
            hide_index=True,
            use_container_width=True
        )

# --- TRACK 2: MALNUTRITION (ALTAIR CHART) ---
else:
    st.title("🥗 Child Malnutrition Analysis")
    
    # Dynamic Metric based on the latest year in CSV
    latest_year = int(df_trends['Year'].dropna().iloc[-1])
    latest_stunting = df_trends['Stunting_Rate'].dropna().iloc[-1]
    
    st.metric(
        label=f"National Stunting Rate ({latest_year})", 
        value=f"{latest_stunting:.1f}%", 
        delta="-2.1%", 
        delta_color="inverse"
    )
    
    st.markdown(f"#### National Stunting Progress (1990 - {latest_year})")
    
    # Altair Chart Setup
    chart_data = df_trends[['Year', 'Stunting_Rate']].dropna()
    
    chart = alt.Chart(chart_data).mark_line(
        point=True, 
        color='#2A9D8F'
    ).encode(
        x=alt.X('Year:O', title='Survey Year (DHS/MICS)'), # :O removes the comma
        y=alt.X('Stunting_Rate:Q', title='Prevalence (%)', scale=alt.Scale(domain=[0, 60])),
        tooltip=['Year', 'Stunting_Rate']
    ).properties(height=450)
    
    st.altair_chart(chart, use_container_width=True)

    #track 3......
    
    # Professional Caption for Transparency
    st.caption(f"""
        **Data Insight:** The visualization concludes in {latest_year} based on the most recent 
        official survey cycle integrated into the dataset. National health surveys 
        are typically conducted every 3-5 years, leading to a reporting lag.
    """)