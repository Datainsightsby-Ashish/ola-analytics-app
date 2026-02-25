import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import mysql.connector

# ------------------------------
# PAGE CONFIG
# ------------------------------
st.set_page_config(page_title="Analytics Dashboard", layout="wide")

st.title("SQL + Power BI Analytics App")

# ------------------------------
# DATABASE CONNECTION FUNCTION
# ------------------------------
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Ashish@123",
        database="ola_project"
    )

def load_data():
    conn = get_connection()
    query = "SELECT * FROM rides"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# ------------------------------
# LOAD DATA
# ------------------------------
df = load_data()

# ------------------------------
# SIDEBAR FILTERS
# ------------------------------
st.sidebar.header("Filters")

# Category Filter (dynamic)
if "category" in df.columns:
    selected_category = st.sidebar.selectbox(
        "Select Category",
        ["All"] + list(df["category"].dropna().unique())
    )
else:
    selected_category = "All"

# Numeric Filter Example (if sales column exists)
if "sales" in df.columns:
    min_sales = int(df["sales"].min())
    max_sales = int(df["sales"].max())
    sales_range = st.sidebar.slider(
        "Sales Range",
        min_sales,
        max_sales,
        (min_sales, max_sales)
    )
else:
    sales_range = None

# Search Box
search_term = st.sidebar.text_input("Search Anything")

# ------------------------------
# APPLY FILTERS
# ------------------------------
filtered_df = df.copy()

if selected_category != "All":
    filtered_df = filtered_df[filtered_df["category"] == selected_category]

if sales_range:
    filtered_df = filtered_df[
        (filtered_df["sales"] >= sales_range[0]) &
        (filtered_df["sales"] <= sales_range[1])
    ]

if search_term:
    filtered_df = filtered_df[
        filtered_df.apply(
            lambda row: search_term.lower() in str(row).lower(),
            axis=1
        )
    ]

# ------------------------------
# KPI SECTION
# ------------------------------
st.subheader("Key Metrics")

col1, col2, col3 = st.columns(3)

col1.metric("Total Rows", len(filtered_df))

if "sales" in filtered_df.columns:
    col2.metric("Total Sales", int(filtered_df["sales"].sum()))

if "category" in filtered_df.columns:
    col3.metric("Unique Categories", filtered_df["category"].nunique())

# ------------------------------
# DATA TABLE
# ------------------------------
st.subheader("SQL Data Results")
st.dataframe(filtered_df, use_container_width=True)

# ------------------------------
# POWER BI EMBED
# ------------------------------
st.subheader("Power BI Dashboard")

powerbi_url = "https://app.powerbi.com/view?r=eyJrIjoiZTI2OTQ0NTAtODg0NS00ZjUzLTg5NDItMDA2MWJjZjkyZWMzIiwidCI6ImM2ZTU0OWIzLTVmNDUtNDAzMi1hYWU5LWQ0MjQ0ZGM1YjJjNCJ9"

components.iframe(
    powerbi_url,
    height=800,
    scrolling=True
)

# ------------------------------
# CLEAN UI (Optional)
# ------------------------------
hide_menu = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
"""
st.markdown(hide_menu, unsafe_allow_html=True)