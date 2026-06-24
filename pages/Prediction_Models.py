import streamlit as st
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

st.title("🤖 Prediction Models")

@st.cache_data
def load_data():
    return pd.read_csv("D2C_Furniture_Transactions.csv")

df = load_data()

# Data Preparation
features = ['Age', 'Product_Price_INR', 'Discount_Applied_%', 'Delivery_Time_Days', 'Satisfaction_Score']
X = df[features].copy()
y = df['Repeat_Purchase'].apply(lambda x: 1 if x == 'Yes' else 0)

# Training
model = RandomForestClassifier(random_state=42)
model.fit(X, y)

st.write(f"Model Accuracy: {model.score(X, y):.2%}")
st.write("Model trained successfully on:", features)
