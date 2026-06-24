import streamlit as st
import pandas as pd
import plotly.express as px

st.title("🎯 Customer Segmentation")
df = pd.read_csv("D2C_Furniture_Transactions.csv")

fig = px.scatter(df, x="Age", y="Final_Order_Value_INR", color="Product_Category", title="Revenue by Age and Category")
st.plotly_chart(fig, use_container_width=True)
