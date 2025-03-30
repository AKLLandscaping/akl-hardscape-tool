import streamlit as st
from utils import (
    load_paver_data, calculate_material_cost, calculate_gravel_cost,
    calculate_fabric_cost, calculate_polymeric_sand, calculate_labor_cost,
    calculate_equipment_cost, calculate_travel_cost, calculate_total
)

st.set_page_config(page_title="AKL Hardscape Master Tool", layout="centered")
st.title("🧱 AKL Hardscape Master Tool")

section = st.radio("📂 Select Project Section", ["Walkway", "Retaining Wall", "Steps", "Fire Pit", "Quote Preview"])

if section == "Walkway":
    st.subheader("🚶 Walkway Estimator")

    sqft = st.number_input("📐 Square Feet", min_value=0)

    # Load product data
    data = load_paver_data()

    # Show only necessary columns
    preview_columns = ["Products", "Pallet Qty", "Unit", "Contractor", "Net", "Margin", "Total", "Coverage"]
    st.markdown("### 🧾 Product List")
    st.dataframe(data[preview_columns])

    # Product selection
    product_names = data["Products"].dropna().unique()
    product = st.selectbox("Choose Material", product_names)

    # Margin input
    margin_percent = st.slider("🧮 Margin %", min_value=0, max_value=100, value=30)
    margin = margin_percent / 100.0

    # Optional add-ons
    include_lifter = st.checkbox("
