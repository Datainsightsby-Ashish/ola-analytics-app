import streamlit as st
import streamlit.components.v1 as components
import pandas as pd

# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------
st.set_page_config(
    page_title="Ride Operations & Revenue Intelligence",
    layout="wide"
)

st.title("Ride Operations & Revenue Intelligence Dashboard")
st.markdown(
    "Operational performance analytics integrating structured ride data with executive-level BI reporting."
)

st.divider()

# ---------------------------------------------------------
# LOAD DATA (CACHED)
# ---------------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("ola_cleaned.csv")
    return df

df = load_data()

# ---------------------------------------------------------
# SIDEBAR FILTERS
# ---------------------------------------------------------
st.sidebar.header("Filters")

vehicle_options = ["All"] + sorted(df["Vehicle_Type"].dropna().unique())
selected_vehicle = st.sidebar.selectbox("Vehicle Type", vehicle_options)

status_options = ["All"] + sorted(df["Booking_Status"].dropna().unique())
selected_status = st.sidebar.selectbox("Booking Status", status_options)

# ---------------------------------------------------------
# APPLY FILTERS (ONLY ONCE)
# ---------------------------------------------------------
filtered_df = df

if selected_vehicle != "All":
    filtered_df = filtered_df[
        filtered_df["Vehicle_Type"] == selected_vehicle
    ]

# KPI dataset (before booking filter)
kpi_df = filtered_df

if selected_status != "All":
    filtered_df = filtered_df[
        filtered_df["Booking_Status"] == selected_status
    ]

# ---------------------------------------------------------
# KPI CALCULATIONS (FAST)
# ---------------------------------------------------------
total_rides = len(kpi_df)

successful_rides = (kpi_df["Booking_Status"] == "Success").sum()
cancelled_rides = total_rides - successful_rides

cancellation_rate = (
    round((cancelled_rides / total_rides) * 100, 2)
    if total_rides > 0 else 0
)

# ---------------------------------------------------------
# NUMBER FORMATTER
# ---------------------------------------------------------
def format_number(num):
    if num >= 1_000_000:
        return f"{num/1_000_000:.1f}M"
    elif num >= 1_000:
        return f"{num/1_000:.1f}K"
    return str(num)

# ---------------------------------------------------------
# KPI DISPLAY
# ---------------------------------------------------------
st.subheader("Executive Key Metrics")

col1, col2, col3 = st.columns(3)

col1.metric("Total Rides", format_number(total_rides))
col2.metric("Successful Rides", format_number(successful_rides))
col3.metric("Cancellation Rate (%)", cancellation_rate)

st.divider()

# ---------------------------------------------------------
# POWER BI (STATIC — DO NOT RELOAD UNNECESSARILY)
# ---------------------------------------------------------
st.subheader("Strategic Performance Dashboard")

components.iframe(
    "https://app.powerbi.com/view?r=eyJrIjoiZDZlYmIwN2UtYjExOC00ZTM1LTkyY2EtYWY1YjVhYmMyYzQ4IiwidCI6ImM2ZTU0OWIzLTVmNDUtNDAzMi1hYWU5LWQ0MjQ0ZGM1YjJjNCJ9",
    height=780
)

st.divider()

# ---------------------------------------------------------
# TABLE (LIMIT ROWS FOR SPEED)
# ---------------------------------------------------------
st.subheader("Operational Data Drill-down")

st.dataframe(
    filtered_df,
    use_container_width=True,
    height=450
)

# ---------------------------------------------------------
# CLEAN FOOTER
# ---------------------------------------------------------
st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)


