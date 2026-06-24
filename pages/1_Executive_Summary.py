import streamlit as st
import pandas as pd
import plotly.express as px

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="Executive Summary", layout="wide")

# ---------- LOAD DATA ----------
df = pd.read_csv("FurniDirect_Customer_Transactions.csv")

# ---------- LOGO ----------
try:
    st.image("logo.png", width=90)
except:
    pass

# ---------- TITLE ----------
st.title("📋 Executive Summary")
st.markdown(
    """
    Welcome to **FurniSense-AI**, a data-driven growth intelligence platform
    developed for a D2C furniture startup operating across Tier 1 and Tier 2 cities in India.

    This dashboard provides actionable insights to understand customer behavior,
    optimize product strategy, improve retention, and support future expansion.
    """
)

st.divider()

# ---------- KPI CALCULATIONS ----------
total_orders = len(df)
total_revenue = df["Final Order Value (INR)"].sum()
avg_order_value = df["Final Order Value (INR)"].mean()
avg_satisfaction = df["Customer Satisfaction Score"].mean()

# ---------- KPI CARDS ----------
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "🛒 Total Orders",
        f"{total_orders:,}"
    )

with col2:
    st.metric(
        "💰 Revenue",
        f"₹{total_revenue:,.0f}"
    )

with col3:
    st.metric(
        "📦 Avg Order Value",
        f"₹{avg_order_value:,.0f}"
    )

with col4:
    st.metric(
        "⭐ Satisfaction",
        round(avg_satisfaction,2)
    )

st.divider()

# ---------- BUSINESS OBJECTIVES ----------
st.subheader("🎯 Business Objectives")

col1, col2 = st.columns(2)

with col1:
    st.info("""
    **Customer Insights**
    
    • Understand customer demographics
    
    • Identify repeat purchase patterns
    
    • Segment customers effectively
    """)

with col2:
    st.success("""
    **Growth Strategy**
    
    • Optimize acquisition channels
    
    • Improve customer satisfaction
    
    • Expand into high-performing cities
    """)

st.divider()

# ---------- REVENUE BY PRODUCT ----------
st.subheader("🪑 Revenue Contribution by Product Category")

revenue_product = (
    df.groupby("Product Category")["Final Order Value (INR)"]
    .sum()
    .reset_index()
)

fig = px.bar(
    revenue_product,
    x="Product Category",
    y="Final Order Value (INR)",
    color="Product Category",
    text_auto=True,
    title="Revenue by Product Category"
)

fig.update_layout(
    template="plotly_white",
    height=500
)

st.plotly_chart(fig, use_container_width=True)

# ---------- CITY TIER DISTRIBUTION ----------
st.subheader("🏙 Customer Distribution by City Tier")

tier_counts = (
    df["City Tier"]
    .value_counts()
    .reset_index()
)

tier_counts.columns = ["City Tier", "Count"]

fig2 = px.pie(
    tier_counts,
    names="City Tier",
    values="Count",
    hole=0.55,
    title="Tier 1 vs Tier 2 Customers"
)

fig2.update_layout(height=450)

st.plotly_chart(fig2, use_container_width=True)

st.divider()

# ---------- KEY INSIGHTS ----------
st.subheader("📌 Key Insights")

st.markdown("""
### ✅ Major Findings

- Tier 1 cities contribute the highest revenue.
- Sofa and Bed categories generate significant order values.
- Longer delivery times negatively affect customer satisfaction.
- Referral and Instagram channels drive strong conversions.
- High satisfaction scores lead to repeat purchases.
- Returns are concentrated within a few product categories.

### 🚀 Recommendations

- Focus marketing budgets on high-converting channels.
- Improve delivery efficiency to enhance customer retention.
- Increase inventory for top-performing categories.
- Expand operations into promising Tier 2 markets.
- Use customer segmentation to personalize promotions.
""")

st.divider()

st.success("✅ FurniSense-AI provides a complete overview of customer behavior, revenue performance, and growth opportunities for the D2C furniture startup.")
