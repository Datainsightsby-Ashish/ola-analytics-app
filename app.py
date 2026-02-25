import streamlit as st
import streamlit.components.v1 as components
import pandas as pd

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="Ola Ride Analytics Dashboard",
    layout="wide"
)

st.title("🚖 SQL + Power BI Analytics App")

# --------------------------------------------------
# LOAD DATA (FROM CSV FOR CLOUD DEPLOYMENT)
# --------------------------------------------------
@st.cache_data
def load_data():
    return pd.read_csv("ola_cleaned.csv")

df = load_data()

# --------------------------------------------------
# SIDEBAR FILTERS
# --------------------------------------------------
st.sidebar.header("🔎 Filters")

# Search
search_term = st.sidebar.text_input("Search Anything")

# Booking Status Filter
if "Booking_Status" in df.columns:
    status_filter = st.sidebar.multiselect(
        "Booking Status",
        options=df["Booking_Status"].unique()
    )
else:
    status_filter = []

# Vehicle Type Filter
if "Vehicle_Type" in df.columns:
    vehicle_filter = st.sidebar.multiselect(
        "Vehicle Type",
        options=df["Vehicle_Type"].unique()
    )
else:
    vehicle_filter = []

# --------------------------------------------------
# APPLY FILTERS
# --------------------------------------------------
filtered_df = df.copy()

if status_filter:
    filtered_df = filtered_df[
        filtered_df["Booking_Status"].isin(status_filter)
    ]

if vehicle_filter:
    filtered_df = filtered_df[
        filtered_df["Vehicle_Type"].isin(vehicle_filter)
    ]

if search_term:
    filtered_df = filtered_df[
        filtered_df.apply(
            lambda row: search_term.lower() in str(row).lower(),
            axis=1
        )
    ]

# --------------------------------------------------
# KPI SECTION
# --------------------------------------------------
st.subheader("📊 Key Metrics")

total_bookings = len(filtered_df)

if "Booking_Status" in filtered_df.columns:
    cancelled = len(filtered_df[
        filtered_df["Booking_Status"] != "Success"
    ])
else:
    cancelled = 0

success_rate = (
    round((total_bookings - cancelled) / total_bookings * 100, 2)
    if total_bookings > 0 else 0
)

col1, col2, col3 = st.columns(3)

col1.metric("Total Bookings", total_bookings)
col2.metric("Cancelled Rides", cancelled)
col3.metric("Success Rate (%)", success_rate)

# --------------------------------------------------
# POWER BI DASHBOARD (MAIN INSIGHT SECTION)
# --------------------------------------------------
st.subheader("📈 Power BI Dashboard")

powerbi_url = "https://app.powerbi.com/view?r=eyJrIjoiZTI2OTQ0NTAtODg0NS00ZjUzLTg5NDItMDA2MWJjZjkyZWMzIiwidCI6ImM2ZTU0OWIzLTVmNDUtNDAzMi1hYWU5LWQ0MjQ0ZGM1YjJjNCJ9"

components.iframe(
    powerbi_url,
    height=750
)

# --------------------------------------------------
# SQL DATA TABLE (DRILL-DOWN)
# --------------------------------------------------
st.subheader("🗂 Detailed Ride Data")

st.dataframe(
    filtered_df,
    use_container_width=True,
    height=450
)

# --------------------------------------------------
# OPTIONAL CLEAN UI
# --------------------------------------------------
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
