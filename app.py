import streamlit as st
import pandas as pd

st.set_page_config(page_title="FurniSense AI", layout="wide")
st.title("FurniSense AI: D2C Analytics")

@st.cache_data
def load_data():
    return pd.read_csv("D2C_Furniture_Transactions.csv")

df = load_data()

st.subheader("Executive Summary")
col1, col2, col3 = st.columns(3)
col1.metric("Total Orders", f"{len(df):,}")
col2.metric("Total Revenue", f"₹{df['Final_Order_Value_INR'].sum():,.0f}")
col3.metric("Avg Satisfaction", f"{df['Satisfaction_Score'].mean():.1f}/5")

st.write("### Data Preview", df.head())
