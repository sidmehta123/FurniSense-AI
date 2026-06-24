import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Prescriptive Analysis", layout="wide")

# ---------------- LOAD DATA ----------------
@st.cache_data
def load_data():
    return pd.read_csv("D2C_Furniture_Transactions.csv")

df = load_data()

# ---------------- TITLE & HEADER ----------------
st.title("💡 Prescriptive Analysis & Strategy")
st.markdown(
"""
Translating predictive insights into **actionable business strategies**. 
Use the scenario planner below to simulate how operational improvements 
directly impact customer retention and bottom-line revenue.
"""
)
st.divider()

# ================= STRATEGY MATRIX =================
st.subheader("🎯 Core Business Strategies")

col1, col2, col3 = st.columns(3)

with col1:
    st.info("""
    ### 📢 Marketing
    **Stop blanket discounting.** * Shift ₹500k from generic Instagram discounts to a targeted "Referral & Loyalty" program for 'High Value' customers.
    * Use our Market Basket rules (Bed → Décor) to trigger automated, personalized post-purchase emails.
    """)

with col2:
    st.warning("""
    ### 🚚 Logistics
    **Fix the 10-day churn threshold.** * Customers experiencing >10 days delivery time drop below a 3.5 satisfaction score and rarely return.
    * Invest in a localized micro-warehouse in our top-performing Tier 2 cities (e.g., Jaipur) to cut transit times.
    """)

with col3:
    st.success("""
    ### 🪑 Product
    **Double down on Sofas & Beds.** * These categories drive the highest revenue but also face higher return rates due to sizing/expectations.
    * Invest in AR (Augmented Reality) features on the app so customers can "see" the sofa in their room before buying.
    """)

st.divider()

# ================= WHAT-IF SCENARIO SIMULATOR =================
st.subheader("🎛️ 'What-If' Scenario Simulator: Logistics Investment")
st.markdown("Adjust the sliders to see how improving average delivery time impacts overall revenue and retention.")

# Current Baseline Metrics
current_avg_delivery = df['Delivery_Time_Days'].mean()
current_retention_rate = (df['Repeat_Purchase'] == 'Yes').mean() * 100
current_revenue = df['Final_Order_Value_INR'].sum()

# Interactive Controls
sim_col, chart_col = st.columns([1, 2])

with sim_col:
    st.markdown("#### Scenario Variables")
    target_delivery = st.slider(
        "Target Average Delivery Time (Days)", 
        min_value=3, 
        max_value=int(current_avg_delivery + 5), 
        value=int(current_avg_delivery),
        step=1
    )
    
    # Simulation Logic (Proxy calculations based on our ML findings)
    # Every day saved increases retention by ~1.5% and boosts lifetime revenue
    day_difference = current_avg_delivery - target_delivery
    
    simulated_retention = min(100, current_retention_rate + (day_difference * 1.5))
    revenue_boost_multiplier = 1 + (day_difference * 0.02) # 2% total revenue boost per day saved
    simulated_revenue = current_revenue * revenue_boost_multiplier

    # Display simulated KPIs
    st.markdown("#### Projected Impact")
    st.metric(
        "Simulated Retention Rate", 
        f"{simulated_retention:.1f}%", 
        f"{simulated_retention - current_retention_rate:+.1f}% vs Current"
    )
    st.metric(
        "Simulated Annual Revenue", 
        f"₹{simulated_revenue:,.0f}", 
        f"₹{simulated_revenue - current_revenue:+,.0f} vs Current"
    )

with chart_col:
    # Create a waterfall chart to show the revenue bridge
    fig_waterfall = go.Figure(go.Waterfall(
        name="Revenue Projection",
        orientation="v",
        measure=["absolute", "relative", "total"],
        x=["Current Revenue", "Logistics Improvement Impact", "Projected Revenue"],
        textposition="outside",
        text=[f"₹{current_revenue:,.0f}", f"+₹{simulated_revenue - current_revenue:,.0f}", f"₹{simulated_revenue:,.0f}"],
        y=[current_revenue, simulated_revenue - current_revenue, simulated_revenue],
        connector={"line": {"color": "rgb(63, 63, 63)"}},
        decreasing={"marker": {"color": "red"}},
        increasing={"marker": {"color": "green"}},
        totals={"marker": {"color": "blue"}}
    ))
    
    fig_waterfall.update_layout(
        title="Revenue Bridge: The Value of Faster Delivery",
        template="plotly_white",
        height=400,
        showlegend=False
    )
    st.plotly_chart(fig_waterfall, use_container_width=True)

st.divider()

# ================= ACTION PLAN =================
st.subheader("📋 Next 90 Days Execution Plan")

execution_data = pd.DataFrame({
    "Phase": ["Phase 1 (Days 1-30)", "Phase 2 (Days 31-60)", "Phase 3 (Days 61-90)"],
    "Initiative": [
        "Deploy 'At-Risk' automated discount emails for delayed deliveries.",
        "Launch 'Living Room Bundle' (Sofa + Storage) ad campaigns on Google.",
        "Secure micro-warehouse lease in Jaipur to reduce Tier 2 delivery times."
    ],
    "Owner": ["Marketing Ops", "Growth Team", "Supply Chain Lead"],
    "Expected ROI": ["High", "Medium", "Very High"]
})

st.dataframe(execution_data, use_container_width=True, hide_index=True)
