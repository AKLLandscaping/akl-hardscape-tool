import streamlit as st
from utils import (
    load_paver_data, load_wall_data, load_steps_data, load_firepit_data,
    calculate_material_cost, calculate_gravel_cost, calculate_fabric_cost,
    calculate_polymeric_sand, calculate_labor_cost, calculate_equipment_cost,
    calculate_travel_cost, calculate_total
)

st.set_page_config(page_title="AKL Hardscape Master Tool", layout="centered")
st.title("🧱 AKL Hardscape Master Tool")

section = st.radio("📂 Select Project Section", ["Walkway", "Retaining Wall", "Steps", "Fire Pit"])

if section == "Walkway":
    st.subheader("🚶 Walkway Estimator")

    # Input: Square footage
    sqft = st.number_input("📐 Square Feet", min_value=0)

    # Load paver products
    paver_data = load_paver_data()
    product_options = paver_data["Product"].dropna().unique()
    selected_product = st.selectbox("🧱 Select Paver Material", product_options)

    # Margin
    margin_override = st.slider("📊 Margin %", min_value=0, max_value=100, value=30)

    # Optional lifter
    include_lifter = st.checkbox("Include Lifter Rental ($100)", value=False)

    # Gravel
    st.markdown("### 🪨 Gravel Base")
    include_gravel = st.checkbox("Include Gravel Base", value=True)
    gravel_depth = st.number_input("Gravel Depth (inches)", value=6.0)
    gravel_cost = 0
    if include_gravel:
        gravel_cost, volume, loads = calculate_gravel_cost(sqft, gravel_depth)
        st.markdown(f"➡️ Volume: {volume} yd³ | Loads: {loads} | Cost: ${gravel_cost:.2f}")

    # Fabric
    include_fabric = st.checkbox("Include Geotextile Fabric ($0.50/sqft)", value=True)
    fabric_cost = calculate_fabric_cost(sqft) if include_fabric else 0

    # Polymeric Sand
    bags, sand_cost = calculate_polymeric_sand(sqft, selected_product)
    st.markdown(f"🧪 Polymeric Sand: {bags} bags @ $50 = ${sand_cost:.2f}")

    # Labor
    st.markdown("### 👷 Labor")
    num_laborers = st.slider("Number of Laborers", 1, 4, value=2)
    hours = st.number_input("Hours per Laborer", min_value=1.0, value=8.0)
    rate = st.selectbox("Labor Rate", [35, 40, 45, 50, 55, 60, 65], index=2)
    labor_cost = calculate_labor_cost(num_laborers, hours, rate)

    # Equipment
    st.markdown("### 🚜 Equipment")
    excavator = st.checkbox("Excavator ($400)")
    skid_steer = st.checkbox("Skid Steer ($350)")
    dump_truck = st.checkbox("Dump Truck ($300)")
    equipment_cost = calculate_equipment_cost(excavator, skid_steer, dump_truck)

    # Travel
    st.markdown("### 🚗 Travel Costs")
    trailer_km = st.number_input("Trailer Travel Distance (km)", min_value=0)
    passenger_km = st.number_input("Passenger Vehicle Distance (km)", min_value=0)
    travel_cost = calculate_travel_cost(trailer_km, passenger_km)

    # Material
    material_cost = calculate_material_cost(selected_product, sqft, paver_data, margin_override)

    # Optional lifter fee
    lifter_cost = 100 if include_lifter else 0

    # Totals
    subtotal, hst, total = calculate_total(
        material_cost, gravel_cost, fabric_cost, sand_cost,
        labor_cost, equipment_cost, travel_cost, lifter_cost
    )

    st.markdown("---")
    st.markdown("## 📊 Summary")
    st.markdown(f"**Material Cost:** ${material_cost:.2f}")
    st.markdown(f"**Gravel:** ${gravel_cost:.2f}")
    st.markdown(f"**Fabric:** ${fabric_cost:.2f}")
    st.markdown(f"**Sand:** ${sand_cost:.2f}")
    st.markdown(f"**Labor:** ${labor_cost:.2f}")
    st.markdown(f"**Equipment:** ${equipment_cost:.2f}")
    st.markdown(f"**Travel:** ${travel_cost:.2f}")
    if lifter_cost:
        st.markdown(f"**Lifter Rental:** ${lifter_cost:.2f}")
    st.markdown(f"**Subtotal:** ${subtotal:.2f}")
    st.markdown(f"**HST (15%):** ${hst:.2f}")
    st.markdown(f"### 💰 Grand Total: ${total:.2f}")
