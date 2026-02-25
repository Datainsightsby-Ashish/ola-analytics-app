import streamlit as st
import streamlit.components.v1 as components
import pandas as pd

# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------
st.set_page_config(
    page_title="Ride Operations & Revenue Intelligence",
    layout="wide"
)

# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------
st.title("Ride Operations & Revenue Intelligence Dashboard")
st.markdown(
    "Operational performance analytics integrating structured ride data with executive-level BI reporting."
)

st.divider()

# ---------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------
@st.cache_data
def load_data():
    return pd.read_csv("ola_cleaned.csv")

df = load_data()

# ---------------------------------------------------------
# SIDEBAR FILTERS
# ---------------------------------------------------------
st.sidebar.header("Filters")

# Vehicle Type Filter (Primary KPI Filter)
vehicle_options = ["All"] + sorted(df["Vehicle_Type"].dropna().unique().tolist())
selected_vehicle = st.sidebar.selectbox(
    "Vehicle Type",
    vehicle_options
)

# Booking Status Filter (Table-only filter)
status_options = ["All"] + sorted(df["Booking_Status"].dropna().unique().tolist())
selected_status = st.sidebar.selectbox(
    "Booking Status",
    status_options
)

# ---------------------------------------------------------
# KPI DATASET (ONLY VEHICLE FILTER APPLIED)
# ---------------------------------------------------------
kpi_df = df.copy()

if selected_vehicle != "All":
    kpi_df = kpi_df[
        kpi_df["Vehicle_Type"] == selected_vehicle
    ]

# ---------------------------------------------------------
# KPI CALCULATIONS (LOGICALLY CORRECT)
# ---------------------------------------------------------
total_rides = len(kpi_df)

successful_rides = len(
    kpi_df[kpi_df["Booking_Status"] == "Success"]
)

cancelled_rides = len(
    kpi_df[kpi_df["Booking_Status"] != "Success"]
)

cancellation_rate = (
    round((cancelled_rides / total_rides) * 100, 2)
    if total_rides > 0 else 0
)

# ---------------------------------------------------------
# FORMAT NUMBERS (K / M)
# ---------------------------------------------------------
def format_number(num):
    if num >= 1_000_000:
        return f"{num/1_000_000:.1f}M"
    elif num >= 1_000:
        return f"{num/1_000:.1f}K"
    else:
        return str(num)

# ---------------------------------------------------------
# DISPLAY KPIs
# ---------------------------------------------------------
st.subheader("Executive Key Metrics")

col1, col2, col3 = st.columns(3)

col1.metric("Total Rides", format_number(total_rides))
col2.metric("Successful Rides", format_number(successful_rides))
col3.metric("Cancellation Rate (%)", cancellation_rate)

st.divider()

# ---------------------------------------------------------
# POWER BI DASHBOARD (STATIC)
# ---------------------------------------------------------
st.subheader("Strategic Performance Dashboard")

powerbi_url = "https://app.powerbi.com/view?r=eyJrIjoiZTI2OTQ0NTAtODg0NS00ZjUzLTg5NDItMDA2MWJjZjkyZWMzIiwidCI6ImM2ZTU0OWIzLTVmNDUtNDAzMi1hYWU5LWQ0MjQ0ZGM1YjJjNCJ9"

components.iframe(
    powerbi_url,
    height=780
)

st.divider()

# ---------------------------------------------------------
# TABLE DATASET (BOTH FILTERS APPLIED)
# ---------------------------------------------------------
table_df = kpi_df.copy()

if selected_status != "All":
    table_df = table_df[
        table_df["Booking_Status"] == selected_status
    ]

# ---------------------------------------------------------
# DISPLAY TABLE
# ---------------------------------------------------------
st.subheader("Operational Data Drill-down")

st.dataframe(
    table_df,
    use_container_width=True,
    height=450
)

# ---------------------------------------------------------
# REMOVE STREAMLIT FOOTER
# ---------------------------------------------------------
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
