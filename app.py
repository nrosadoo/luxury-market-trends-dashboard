
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Luxury Market Dashboard", layout="wide")

st.title(" Luxury Market Trends – SW Florida")

# Load data
@st.cache_data
def load_data():
    return pd.read_csv("data/luxury_real_estate_data.csv", parse_dates=["listing_date"])

df = load_data()

# Sidebar filters
st.sidebar.header("Filter Listings")
zip_filter = st.sidebar.multiselect("Zip Code", options=df["zip_code"].unique(), default=df["zip_code"].unique())
type_filter = st.sidebar.multiselect("Home Type", options=df["home_type"].unique(), default=df["home_type"].unique())

df_filtered = df[(df["zip_code"].isin(zip_filter)) & (df["home_type"].isin(type_filter))]
df_filtered["month"] = df_filtered["listing_date"].dt.to_period("M").astype(str)

# Price per sqft over time
st.subheader(" Price Per Sqft Over Time")
price_trend = df_filtered.groupby(["month", "zip_code"])["price_per_sqft"].mean().reset_index()
fig1 = px.line(price_trend, x="month", y="price_per_sqft", color="zip_code", markers=True)
st.plotly_chart(fig1, use_container_width=True)

# Days on market
st.subheader(" Average Days on Market")
avg_days = df_filtered.groupby("zip_code")["days_on_market"].mean().reset_index()
fig2 = px.bar(avg_days, x="zip_code", y="days_on_market", color="zip_code")
st.plotly_chart(fig2, use_container_width=True)

# Home type size
st.subheader(" Average Home Size by Type")
avg_size = df_filtered.groupby("home_type")["square_feet"].mean().reset_index()
fig3 = px.pie(avg_size, names="home_type", values="square_feet", title="Avg Sq Ft by Home Type")
st.plotly_chart(fig3, use_container_width=True)
