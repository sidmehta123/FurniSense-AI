import streamlit as st
import pandas as pd

st.set_page_config(page_title="Executive Summary", layout="wide")

# Force a fresh read without the memory cache
def load_data():
    return pd.read_csv("D2C_Furniture_Transactions.csv")

df = load_data()

# Print the exact columns to the screen and stop the app from crashing
st.title("🚨 Debug Mode")
st.error("Here are the exact column names Streamlit is currently seeing in the file:")
st.write(df.columns.tolist())
st.stop()
