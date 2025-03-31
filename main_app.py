import streamlit as st
from utils import load_paver_data, calculate_material_cost

st.set_page_config(page_title="AKL Hardscape Master Tool - Walkway Estimator")
st.title("🧱 AKL Hardscape Master Tool")
st.header("🚶‍♂️ Walkway Estimator")

# Load product data
data = load_paver_data()
products = data["Products"].dropna().unique()

# Inputs
sqft = st.number_input("📏 Square Feet", min_value=0, value=0, step=10)
margin_override = st.slider("📊 Override Margin %", 0, 100, 30)
selected_product = st.selectbox("🧱 Choose Product", products)

# Estimate
if sqft > 0 and selected_product:
    cost_data = calculate_material_cost(selected_product, sqft, data, margin_override)

    st.subheader("💰 Estimate Summary")
    st.write(f"**Product:** {selected_product}")
    st.write(f"**Price per Unit (with margin):** ${cost_data['price_per_unit']:.2f}")
    st.write(f"**Units Required:** {cost_data['units_required']}")
    st.write(f"**Material Total:** ${cost_data['material_total']:.2f}")
