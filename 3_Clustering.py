import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.decomposition import PCA

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Customer Segmentation", layout="wide")

# ---------------- LOAD DATA ----------------
@st.cache_data
def load_data():
    # Make sure this matches the filename of your generated dataset
    return pd.read_csv("D2C_Furniture_Transactions.csv") 

df = load_data()

# ---------------- TITLE & HEADER ----------------
st.title("🎯 Customer Segmentation (Clustering)")
st.markdown(
"""
Using **K-Means Clustering**, we have segmented your customer base into distinct groups 
based on their purchasing behavior, satisfaction, and demographics. 
This allows for highly targeted marketing and operational improvements.
"""
)
st.divider()

# ================= CLUSTERING LOGIC =================
# Select numerical features for clustering
features = [
    "Final_Order_Value_INR", 
    "Satisfaction_Score", 
    "Delivery_Time_Days", 
    "Discount_Applied_%", 
    "Age"
]

# Drop missing values in these features (if any)
cluster_data = df.dropna(subset=features).copy()

# Standardize the data so larger numbers (like INR) don't dominate smaller ones (like Score)
scaler = StandardScaler()
scaled_data = scaler.fit_transform(cluster_data[features])

# Apply K-Means Machine Learning Algorithm
kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
cluster_data["Cluster"] = kmeans.fit_predict(scaled_data)

# Calculate cluster centers to determine which cluster is which
cluster_means = cluster_data.groupby("Cluster")[features].mean()

# Simple logic to map clusters to business personas based on Order Value and Satisfaction
cluster_data["Persona"] = cluster_data["Cluster"].map({
    0: "High Value & Loyal 💎",
    1: "Discount Seekers 🏷️",
    2: "At-Risk / Delayed ⚠️"
})

# ================= CLUSTER SUMMARY CARDS =================
st.subheader("👥 Customer Segments Overview")

col1, col2, col3 = st.columns(3)
cluster_counts = cluster_data["Persona"].value_counts()

with col1:
    st.info(f"**{cluster_counts.index[0]}**\n\nTotal Customers: **{cluster_counts.iloc[0]}**")
with col2:
    st.success(f"**{cluster_counts.index[1]}**\n\nTotal Customers: **{cluster_counts.iloc[1]}**")
with col3:
    st.warning(f"**{cluster_counts.index[2]}**\n\nTotal Customers: **{cluster_counts.iloc[2]}**")

st.divider()

# ================= VISUALIZATIONS =================
col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    st.subheader("📊 PCA Cluster Visualization")
    st.markdown("A 2D machine learning projection of multi-dimensional customer data.")
    
    # PCA reduces our 5 variables into 2 dimensions so we can plot them on an X/Y axis
    pca = PCA(n_components=2)
    pca_result = pca.fit_transform(scaled_data)
    cluster_data["PCA1"] = pca_result[:, 0]
    cluster_data["PCA2"] = pca_result[:, 1]
    
    fig_pca = px.scatter(
        cluster_data, 
        x="PCA1", 
        y="PCA2", 
        color="Persona",
        color_discrete_sequence=['#636EFA', '#00CC96', '#EF553B'],
        opacity=0.75,
        hover_data=["Final_Order_Value_INR", "Delivery_Time_Days", "Satisfaction_Score"]
    )
    fig_pca.update_layout(template="plotly_white", height=450)
    st.plotly_chart(fig_pca, use_container_width=True)

with col_chart2:
    st.subheader("🕸️ Cluster Radar Chart")
    st.markdown("Comparing the average traits of each customer persona.")
    
    # Get mean values for the radar chart
    radar_means = cluster_data.groupby("Persona")[features].mean().reset_index()
    
    # MinMax Scale the means so they fit perfectly on a 0-1 radar chart scale
    radar_scaler = MinMaxScaler()
    scaled_means = radar_scaler.fit_transform(radar_means[features])
    
    fig_radar = go.Figure()
    colors = ['#636EFA', '#00CC96', '#EF553B']
    
    # Format feature names for better readability on the chart
    clean_features = ["Order Value", "Satisfaction", "Delivery Time", "Discount %", "Age"]
    
    for i, row in enumerate(scaled_means):
        fig_radar.add_trace(go.Scatterpolar(
            r=row.tolist() + [row[0]], # Close the polygon loop
            theta=clean_features + [clean_features[0]],
            fill='toself',
            name=radar_means['Persona'].iloc[i],
            line_color=colors[i % len(colors)]
        ))

    fig_radar.update_layout(
        polar=dict(radialaxis=dict(visible=False)),
        showlegend=True,
        template="plotly
