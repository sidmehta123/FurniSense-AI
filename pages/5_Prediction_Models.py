import os
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
st.divider()

# --- FIX: Mapping to YOUR columns ---
# Using Age_Group (Categorical) instead of Age (Numeric)
# Using Average_Order_Value_AED instead of Price
df['Repeat_Purchase_Intention'] = df['Repeat_Purchase_Intention'].astype(str).str.strip().str.title()

features = ['Age_Group', 'Average_Order_Value_AED', 'Discount_Sensitivity_Score', 'Actual_Delivery_Time_Days', 'Customer_Satisfaction_Score']
X = df[features].copy()

# Encode everything since your data is categorical
le = LabelEncoder()
X['Age_Group'] = le.fit_transform(df['Age_Group'].astype(str))
X['City'] = le.fit_transform(df['City'].astype(str))

y = df['Repeat_Purchase_Intention'].apply(lambda x: 1 if x == 'Yes' else 0)

if len(y.unique()) <= 1:
    st.error("⚠️ Data contains only one outcome for Repeat Purchase.")
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
feat_df = pd.DataFrame({'Feature': features, 'Importance': importances}).sort_values(by='Importance', ascending=True)
fig_feat = px.bar(feat_df, x='Importance', y='Feature', orientation='h', title="Top Drivers of Retention")
st.plotly_chart(fig_feat, use_container_width=True)
