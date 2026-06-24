import streamlit as st
import pandas as pd

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="New Customer Scorer", layout="wide")

# ---------------- LOGO ----------------
try:
    st.image("logo.png", width=90)
except:
    pass

# ---------------- TITLE & HEADER ----------------
st.title("👤 New Customer Scorer (Interactive Tool)")
st.markdown(
"""
Use this tool to input a theoretical (or new) customer's profile. 
The system will apply our analytical rules to instantly predict their **Segment**, 
**Retention Probability**, and the best **Next Best Action (NBA)**.
"""
)
st.divider()

# ================= INTERACTIVE FORM =================
st.subheader("📝 Input Customer Data")

# Create a form so the page doesn't refresh on every single click
with st.form("customer_form"):
    col1, col2, col3 = st.columns(3)
    
    with col1:
        age = st.number_input("Customer Age", min_value=18, max_value=80, value=30)
        city_tier = st.selectbox("City Tier", ["Tier 1", "Tier 2"])
        
    with col2:
        category = st.selectbox("Product Bought", ["Bed", "Sofa", "Dining Set", "Storage Unit", "Décor"])
        order_value = st.number_input("Order Value (INR)", min_value=500, max_value=100000, value=25000, step=1000)
        
    with col3:
        delivery_days = st.slider("Delivery Time (Days)", min_value=1, max_value=25, value=7)
        satisfaction = st.slider("Satisfaction Score", min_value=1, max_value=5, value=4)
        
    submit_button = st.form_submit_button(label="Generate Intelligence Report")

st.divider()

# ================= SCORING LOGIC & OUTPUT =================
if submit_button:
    st.subheader("📊 Intelligence Report")
    
    # --- Logic 1: Determine Segment (Proxy logic based on our clustering) ---
    if order_value >= 30000 and satisfaction >= 4:
        segment = "High Value & Loyal 💎"
        color = "green"
    elif order_value < 20000 and satisfaction >= 3:
        segment = "Discount Seeker 🏷️"
        color = "blue"
    elif satisfaction <= 2 or delivery_days >= 12:
        segment = "At-Risk / Delayed ⚠️"
        color = "red"
    else:
        segment = "Standard Customer 👤"
        color = "gray"

    # --- Logic 2: Predict Repeat Purchase (Proxy based on our ML model) ---
    base_prob = 50
    
    # Adjust probability based on features
    if satisfaction == 5: base_prob += 35
    if satisfaction == 4: base_prob += 15
    if satisfaction <= 2: base_prob -= 40
    
    if delivery_days > 10: base_prob -= 20
    if delivery_days <= 5: base_prob += 10
    
    if city_tier == "Tier 1": base_prob += 5
    
    # Ensure it stays between 0 and 100
    retention_prob = max(5, min(95, base_prob))

    # --- Logic 3: Next Best Action (Based on Association Rules & Prescriptive) ---
    if segment == "At-Risk / Delayed ⚠️":
        nba = "IMMEDIATE ACTION: Trigger automated apology email from Founder with a 25% 'Win-Back' discount code."
    elif category == "Bed":
        nba = "CROSS-SELL: Send targeted email highlighting matching Bedroom Décor (Lamps, Rugs) at a 10% bundle discount."
    elif category == "Sofa":
        nba = "CROSS-SELL: Recommend Living Room Storage Units to match the Sofa."
    elif segment == "High Value & Loyal 💎":
        nba = "LOYALTY: Enroll in 'FurniSense Black' tier. Send physical thank-you card and referral code."
    else:
        nba = "NURTURE: Send standard 30-day post-purchase check-in and request a review."

    # --- Display Results ---
    res_col1, res_col2 = st.columns(2)
    
    with res_col1:
        st.markdown(f"### Predicted Segment")
        st.markdown(f"<h2 style='color: {color};'>{segment}</h2>", unsafe_allow_html=True)
        
        st.markdown(f"### Retention Probability")
        
        # Color code the progress bar metric
        if retention_prob >= 70:
            st.success(f"{retention_prob}% chance of returning")
        elif retention_prob >= 40:
            st.warning(f"{retention_prob}% chance of returning")
        else:
            st.error(f"{retention_prob}% chance of returning")
            
        st.progress(retention_prob / 100)

    with res_col2:
        st.markdown("### 🎯 Recommended Next Best Action (NBA)")
        st.info(nba)
        
        st.markdown("### 🧠 Model Reasoning")
        st.markdown(f"""
        * **Delivery Impact:** A delivery time of **{delivery_days} days** strongly influenced the retention score.
        * **Satisfaction Impact:** A score of **{satisfaction}/5** was the primary driver for the Segment assignment.
        * **Market Basket:** The NBA recommendation is directly driven by the purchase of a **{category}**.
        """)
