import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Descriptive Analysis", layout="wide")

# ---------------- LOAD DATA ----------------
df = pd.read_csv("FurniDirect_Customer_Transactions.csv")

# ---------------- LOGO ----------------
try:
    st.image("logo.png", width=90)
except:
    pass

# ---------------- TITLE ----------------
st.title("📈 Descriptive Analysis")
st.markdown(
"""
Explore customer demographics, revenue patterns, delivery performance,
and acquisition channels to understand the key drivers of business growth.
"""
)

st.divider()

# ================= KPI CARDS =================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "💰 Revenue",
        f"₹{df['Final Order Value (INR)'].sum():,.0f}"
    )

with col2:
    st.metric(
        "🛒 Orders",
        f"{len(df):,}"
    )

with col3:
    st.metric(
        "⭐ Avg Satisfaction",
        round(df["Customer Satisfaction Score"].mean(),2)
    )

with col4:
    st.metric(
        "🚚 Avg Delivery Days",
        round(df["Delivery Time (days)"].mean(),1)
    )

st.divider()

# ================= PRODUCT CATEGORY =================

col1, col2 = st.columns(2)

with col1:

    st.subheader("🪑 Orders by Product Category")

    category_count = (
        df["Product Category"]
        .value_counts()
        .reset_index()
    )

    category_count.columns = ["Product Category","Orders"]

    fig1 = px.bar(
        category_count,
        x="Product Category",
        y="Orders",
        color="Product Category",
        text_auto=True
    )

    fig1.update_layout(
        template="plotly_white",
        showlegend=False,
        height=450
    )

    st.plotly_chart(fig1, use_container_width=True)

with col2:

    st.subheader("🏙 Revenue by City")

    city_revenue = (
        df.groupby("City")["Final Order Value (INR)"]
        .sum()
        .reset_index()
        .sort_values(
            by="Final Order Value (INR)",
            ascending=True
        )
    )

    fig2 = px.bar(
        city_revenue,
        x="Final Order Value (INR)",
        y="City",
        orientation="h",
        color="City",
        text_auto=".2s"
    )

    fig2.update_layout(
        template="plotly_white",
        showlegend=False,
        height=450
    )

    st.plotly_chart(fig2, use_container_width=True)

st.divider()

# ================= ACQUISITION CHANNEL =================

col1, col2 = st.columns(2)

with col1:

    st.subheader("📢 Acquisition Channels")

    channel_count = (
        df["Acquisition Channel"]
        .value_counts()
        .reset_index()
    )

    channel_count.columns = ["Channel","Count"]

    fig3 = px.pie(
        channel_count,
        names="Channel",
        values="Count",
        hole=0.6
    )

    fig3.update_layout(height=450)

    st.plotly_chart(fig3, use_container_width=True)

with col2:

    st.subheader("🎂 Customer Age Distribution")

    fig4 = px.histogram(
        df,
        x="Age",
        nbins=20
    )

    fig4.update_layout(
        template="plotly_white",
        height=450
    )

    st.plotly_chart(fig4, use_container_width=True)

st.divider()

# ================= DELIVERY VS SATISFACTION =================

col1, col2 = st.columns(2)

with col1:

    st.subheader("🚚 Delivery Time vs Satisfaction")

    fig5 = px.scatter(
        df,
        x="Delivery Time (days)",
        y="Customer Satisfaction Score",
        color="City Tier",
        opacity=0.7
    )

    fig5.update_layout(
        template="plotly_white",
        height=450
    )

    st.plotly_chart(fig5, use_container_width=True)

with col2:

    st.subheader("🔄 Return Status")

    return_count = (
        df["Return Status"]
        .value_counts()
        .reset_index()
    )

    return_count.columns = ["Return Status","Count"]

    fig6 = px.pie(
        return_count,
        names="Return Status",
        values="Count",
        hole=0.55
    )

    fig6.update_layout(height=450)

    st.plotly_chart(fig6, use_container_width=True)

st.divider()

# ================= CITY TIER SATISFACTION =================

st.subheader("⭐ Satisfaction Score by City Tier")

tier_sat = (
    df.groupby("City Tier")["Customer Satisfaction Score"]
    .mean()
    .reset_index()
)

fig7 = px.bar(
    tier_sat,
    x="City Tier",
    y="Customer Satisfaction Score",
    color="City Tier",
    text_auto=".2f"
)

fig7.update_layout(
    template="plotly_white",
    showlegend=False,
    height=500
)

st.plotly_chart(fig7, use_container_width=True)

st.divider()

# ================= INSIGHTS =================

st.subheader("📌 Key Insights")

st.success("""
### Major Findings

✅ Sofa and Bed categories contribute the highest order volume.

✅ Tier 1 cities generate greater revenue compared to Tier 2 cities.

✅ Customer satisfaction decreases with increasing delivery time.

✅ Instagram Ads and Google Search are major acquisition channels.

✅ Most customers do not return products, indicating healthy service quality.

✅ Younger customers (25–40 years) form the largest customer segment.

### Recommendations

• Reduce delivery times to improve satisfaction.

• Increase marketing investments in top-performing channels.

• Expand operations in high-revenue cities.

• Strengthen inventory planning for high-demand categories.

• Improve after-sales support to minimize returns.
""")
