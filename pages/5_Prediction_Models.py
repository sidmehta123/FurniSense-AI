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

# --- THE FIX: Scrub invisible spaces and force everything to lowercase ---
df['Repeat_Purchase'] = df['Repeat_Purchase'].astype(str).str.strip().str.lower()
df['City_Tier'] = df['City_Tier'].astype(str).str.strip()

features = ['Age', 'Product_Price_INR', 'Discount_Applied_%', 'Delivery_Time_Days', 'Satisfaction_Score']
X = df[features].copy()

le = LabelEncoder()
X['City_Tier_Encoded'] = le.fit_transform(df['City_Tier'])
features.append('City_Tier_Encoded')

# Now it correctly maps 'yes' to 1 and 'no' to 0
y = df['Repeat_Purchase'].apply(lambda x: 1 if x == 'yes' else 0)

# Failsafe check
if len(y.unique()) <= 1:
    st.error("⚠️ Not enough data variety. The model requires both returning and non-returning customers to learn.")
    st.stop()

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)
y_pred = rf_model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

st.subheader("🎯 Model Performance")
col1, col2, col3 = st.columns(3)
with col1: st.metric("Model Used", "Random Forest", "Classification")
with col2: st.metric("Prediction Accuracy", f"{accuracy * 100:.1f}%", "On Unseen Test Data")
with col3: st.metric("Baseline Lift", f"+{(accuracy * 100) - (y.value_counts(normalize=True).max() * 100):.1f}%")

st.divider()

col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    importances = rf_model.feature_importances_
    clean_features = ['Age', 'Price (INR)', 'Discount (%)', 'Delivery Time', 'Satisfaction', 'City Tier']
    feat_df = pd.DataFrame({'Feature': clean_features, 'Importance': importances}).sort_values(by='Importance', ascending=True)

    fig_feat = px.bar(feat_df, x='Importance', y='Feature', orientation='h', color='Importance', color_continuous_scale='Teal')
    fig_feat.update_layout(template="plotly_white", height=400)
    st.plotly_chart(fig_feat, use_container_width=True)

with col_chart2:
    cm = confusion_matrix(y_test, y_pred)
    fig_cm = px.imshow(cm, x=['Pred: No Return', 'Pred: Will Return'], y=['Actual: No Return', 'Actual: Will Return'], text_auto=True, color_continuous_scale='Blues')
    fig_cm.update_layout(template="plotly_white", height=400)
    st.plotly_chart(fig_cm, use_container_width=True)
