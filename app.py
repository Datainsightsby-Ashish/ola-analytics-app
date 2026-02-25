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
# CUSTOM STYLING (Corporate Grey Theme)
# ---------------------------------------------------------
st.markdown("""
<style>
body {
    background-color: #0f172a;
}
h1 {
    font-size: 34px;
    font-weight: 600;
}
.metric-container {
    background-color: #1e293b;
    padding: 18px;
    border-radius: 8px;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# HEADER SECTION
# ---------------------------------------------------------
st.title("Ride Operations & Revenue Intelligence Dashboard")
st.markdown(
    "Operational performance and revenue analytics powered by structured ride data and executive-level BI reporting."
)

st.divider()

# ---------------------------------------------------------
# LOAD DATA (CSV for Cloud Deployment)
# ---------------------------------------------------------
@st.cache_data
def load_data():
    return pd.read_csv("ola_cleaned.csv")

df = load_data()

# ---------------------------------------------------------
# SIDEBAR FILTERS (Clean & Focused)
# ---------------------------------------------------------
st.sidebar.header("Filters")

# Booking Status
status_filter = st.sidebar.multiselect(
    "Booking Status",
    options=sorted(df["Booking_Status"].dropna().unique())
)

# Vehicle Type
vehicle_filter = st.sidebar.multiselect(
    "Vehicle Type",
    options=sorted(df["Vehicle_Type"].dropna().unique())
)

# ---------------------------------------------------------
# APPLY FILTERS
# ---------------------------------------------------------
filtered_df = df.copy()

if status_filter:
    filtered_df = filtered_df[
        filtered_df["Booking_Status"].isin(status_filter)
    ]

if vehicle_filter:
    filtered_df = filtered_df[
        filtered_df["Vehicle_Type"].isin(vehicle_filter)
    ]

# ---------------------------------------------------------
# KPI CALCULATIONS
# ---------------------------------------------------------
total_rides = len(filtered_df)

successful_rides = len(
    filtered_df[filtered_df["Booking_Status"] == "Success"]
)

cancelled_rides = len(
    filtered_df[filtered_df["Booking_Status"] != "Success"]
)

cancellation_rate = (
    round((cancelled_rides / total_rides) * 100, 2)
    if total_rides > 0 else 0
)

# ---------------------------------------------------------
# KPI DISPLAY (Executive Layout)
# ---------------------------------------------------------
st.subheader("Executive Key Metrics")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Revenue", f"{total_revenue:,.0f}")
col2.metric("Total Rides", f"{total_rides:,}")
col3.metric("Successful Rides", f"{successful_rides:,}")
col4.metric("Cancellation Rate (%)", cancellation_rate)

st.divider()

# ---------------------------------------------------------
# POWER BI EMBED (Primary Insight Section)
# ---------------------------------------------------------
st.subheader("Strategic Performance Dashboard")

powerbi_url = "https://app.powerbi.com/view?r=eyJrIjoiZTI2OTQ0NTAtODg0NS00ZjUzLTg5NDItMDA2MWJjZjkyZWMzIiwidCI6ImM2ZTU0OWIzLTVmNDUtNDAzMi1hYWU5LWQ0MjQ0ZGM1YjJjNCJ9"

components.iframe(
    powerbi_url,
    height=780
)

st.divider()

# ---------------------------------------------------------
# DETAILED DATA TABLE (Drill-down Layer)
# ---------------------------------------------------------
st.subheader("Operational Data Drill-down")

st.dataframe(
    filtered_df,
    use_container_width=True,
    height=450
)

# ---------------------------------------------------------
# REMOVE STREAMLIT DEFAULT FOOTER
# ---------------------------------------------------------
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
