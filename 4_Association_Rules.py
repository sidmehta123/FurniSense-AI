import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Market Basket Analysis", layout="wide")

# ---------------- LOGO ----------------
try:
    st.image("logo.png", width=90)
except:
    pass

# ---------------- TITLE ----------------
st.title("🔗 Association Rules (Market Basket Analysis)")
st.markdown(
"""
Using the **Apriori Algorithm**, we analyze historical transaction baskets to discover 
hidden patterns in customer purchasing behavior. This helps in building recommendation 
engines, optimizing website layouts, and creating profitable product bundles.
"""
)
st.divider()

# ================= MOCK APRIORI DATA =================
# For the purpose of this dashboard, we simulate the output of an Apriori model
# showing what products are frequently bought together.
data = {
    "Antecedents (If bought...)": ["Bed", "Sofa", "Dining Set", "Storage Unit", "Bed"],
    "Consequents (...Then buys)": ["Décor", "Storage Unit", "Décor", "Décor", "Storage Unit"],
    "Support (%)": [15.2, 12.8, 10.5, 8.4, 6.1],
    "Confidence (%)": [68.5, 55.2, 48.0, 42.1, 35.5],
    "Lift": [2.4, 1.9, 1.6, 1.3, 1.1]
}
rules_df = pd.DataFrame(data)

# ================= KPI CARDS =================
st.subheader("🛒 Cross-Selling Metrics")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Rules Discovered", "14", "+3 this month")
with col2:
    st.metric("Highest Confidence Rule", "Bed → Décor", "68.5%")
with col3:
    st.metric("Avg Order Value Boost", "₹4,250", "from bundled items")

st.divider()

# ================= VISUALIZATIONS =================
col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    st.subheader("🫧 Rule Strength (Support vs Confidence)")
    st.markdown("Larger bubbles indicate higher **Lift** (strength of the association).")
    
    fig_scatter = px.scatter(
        rules_df, 
        x="Support (%)", 
        y="Confidence (%)", 
        size="Lift", 
        color="Antecedents (If bought...)",
        hover_name="Consequents (...Then buys)",
        size_max=30,
        template="plotly_white"
    )
    fig_scatter.update_layout(height=450)
    st.plotly_chart(fig_scatter, use_container_width=True)

with col_chart2:
    st.subheader("📊 Top Cross-Sell Opportunities")
    st.markdown("Likelihood of buying a second item after the first.")
    
    # Create a cleaner label for the bar chart
    rules_df["Rule"] = rules_df["Antecedents (If bought...)"] + " → " + rules_df["Consequents (...Then buys)"]
    
    fig_bar = px.bar(
        rules_df.sort_values("Confidence (%)", ascending=True),
        x="Confidence (%)",
        y="Rule",
        orientation='h',
        color="Lift",
        color_continuous_scale="Blues",
        text="Confidence (%)"
    )
    fig_bar.update_layout(template="plotly_white", height=450)
    fig_bar.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
    st.plotly_chart(fig_bar, use_container_width=True)

st.divider()

# ================= INTERACTIVE RULE EXPLORER =================
st.subheader("🔍 Explore Recommendations")
selected_product = st.selectbox("Select a product to see what customers buy next:", 
                                ["Bed", "Sofa", "Dining Set", "Storage Unit"])

# Filter rules based on selection
filtered_rules = rules_df[rules_df["Antecedents (If bought...)"] == selected_product]

if not filtered_rules.empty:
    st.dataframe(filtered_rules.drop(columns=["Rule"]), use_container_width=True, hide_index=True)
else:
    st.info(f"No strong association rules found for {selected_product} yet.")

st.divider()

# ================= BUSINESS RECOMMENDATIONS =================
st.subheader("💡 Bundling & Strategy Recommendations")

st.success("""
### 🛏️ Bed & Décor Synergy (Highest Lift: 2.4)
* **Insight:** 68.5% of customers who buy a Bed also buy Décor items (lamps, rugs, wall art).
* **Action:** Implement an "Add to Cart" pop-up for heavily discounted Décor items immediately after a Bed is added to the cart. 

### 🛋️ Sofa & Storage Unit Connection (Lift: 1.9)
* **Insight:** Strong association between living room seating and organizational units.
* **Action:** Create a "Living Room Starter Kit" bundle targeting Tier 1 cities (where apartment space is limited) combining a Sofa + Storage Unit for a 15% combined discount.

### 📉 Low Association Warning
* **Insight:** Dining Sets rarely trigger secondary high-ticket purchases.
* **Action:** Rely on post-purchase email campaigns (sent 2 weeks later) rather than immediate checkout cross-sells to avoid cart abandonment from decision fatigue.
""")
