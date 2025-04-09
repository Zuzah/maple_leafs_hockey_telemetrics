import streamlit as st
import requests
import pandas as pd

BACKEND_URL = "http://backend:8000"

st.set_page_config(page_title="Hockey Telemetrics", layout="wide")
st.title("Maple Leafs Defensemen Metrics Dashboard")

# Fetch Zone Time Data
st.header("Defensive Zone Time per Shift")
zone_time_data = requests.get(f"{BACKEND_URL}/metrics/zone-time").json()
zone_df = pd.DataFrame(zone_time_data)
if not zone_df.empty:
    st.dataframe(zone_df)
    st.bar_chart(zone_df.set_index("player_id")["avg_dz_time_per_shift_secs"])

# Fetch Slot Coverage Data
st.header("Slot Coverage Effectiveness")
slot_data = requests.get(f"{BACKEND_URL}/metrics/slot-coverage").json()
slot_df = pd.DataFrame(slot_data)
if not slot_df.empty:
    st.dataframe(slot_df)
    st.bar_chart(slot_df.set_index("player_id")["slot_coverage_pct"])
