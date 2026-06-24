import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.preprocessing import LabelEncoder

st.set_page_config(page_title="Prediction Models", layout="wide")

@st.cache_data
def load_data():
    return pd.read_csv("D2C_Furniture_Transactions.csv")

df = load_data()

st.title("🤖 Prediction Models (Machine Learning)")

# --- FIX: Mapping to YOUR columns (Age, Product_Price_INR, etc) ---
# Data cleaning: Ensure Repeat_Purchase is clean text
df['Repeat_Purchase'] = df['Repeat_Purchase'].astype(str).str.strip().str.title()

# Use the columns present in your CSV
features = ['Age', 'Product_Price_INR', 'Discount_Applied_%', 'Delivery_Time_Days', 'Satisfaction_Score']
X = df[features].copy()

# Encode Categorical data
le = LabelEncoder()
X['City_Tier'] = le.fit_transform(df['City_Tier'].astype(str))
X['Acquisition_Channel'] = le.fit_transform(df['Acquisition_Channel'].astype(str))

# Map Repeat_Purchase: Yes -> 1, No -> 0
y = df['Repeat_Purchase'].apply(lambda x: 1 if x == 'Yes' else 0)

if len(y.unique()) <= 1:
    st.error("⚠️ The model cannot train because your data only shows one type of customer (e.g., all 'Yes').")
    st.stop()

# Train Model
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)
y_pred = rf_model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

st.subheader("🎯 Model Performance")
st.metric("Prediction Accuracy", f"{accuracy * 100:.1f}%")

# Feature Importance
importances = rf_model.feature_importances_
feat_df = pd.DataFrame({'Feature': features + ['City_Tier', 'Acquisition_Channel'], 'Importance': importances})
feat_df = feat_df.sort_values(by='Importance', ascending=True)
fig_feat = px.bar(feat_df, x='Importance', y='Feature', orientation='h', title="Key Drivers of Repeat Purchase")
st.plotly_chart(fig_feat, use_container_width=True)
