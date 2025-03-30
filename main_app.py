import streamlit as st
from utils import (
    load_paver_data, load_wall_data, load_steps_data, load_firepit_data,
    calculate_material_cost, calculate_gravel_cost, calculate_fabric_cost,
    calculate_polymeric_sand, calculate_labor_cost, calculate_equipment_cost,
    calculate_travel_cost, calculate_total
)

st.set_page_config(page_title="AKL Hardscape Master Tool", layout="centered")
st.title("🧱 AKL Hardscape Master Tool")

section = st.radio("📂 Select Project Section", ["Walkway", "Retaining Wall", "Steps", "Fire Pit", "Quote Preview"])

if section == "Walkway":
    st.header("🚶 Walkway Estimator")

    sqft = st.number_input("📐 Square Feet", min_value=0, value=0)

    # Load and filter product data
    data = load_paver_data()
    product_list = data["Products"].dropna().unique()
    product = st.selectbox("🧱 Choose Material", product_list)

    # 🔧 Margin Selection
    margin_input = st.slider("📊 Margin %", 0, 100, 30)
    margin_decimal = margin_input / 100.0

    # Optional Add-ons
    include_lifter = st.checkbox("Include Lifter Rental ($100)", value=False)

    # Gravel Section
    st.markdown("🪨 **Gravel Base**")
    include_gravel = st.checkbox("Include Gravel Base", value=True)
    gravel_depth = st.number_input("Gravel Depth (inches)", min_value=0.0, max_value=24.0, value=6.0)

    gravel_cost = gravel_volume = gravel_loads = 0
    fabric_cost = 0
    if include_gravel:
        gravel_cost, gravel_volume, gravel_loads = calculate_gravel_cost(sqft, gravel_depth)
        include_fabric = st.checkbox("Include Geotextile Fabric ($0.50/sq ft)", value=True)
        fabric_cost = calculate_fabric_cost(sqft) if include_fabric else 0

    # Sand
    st.markdown("🏖 **Polymeric Sand**")
    bags, sand_cost = calculate_polymeric_sand(sqft, product)
    st.markdown(f"🧂 {bags} bags needed × $50 = **${sand_cost:.2f}**")

    # Labor
    st.markdown("👷 **Labor & Equipment**")
    num_laborers = st.slider("Number of Laborers", 1, 4, 2)
    hours = st.number_input("Hours per Laborer", min_value=0.0, value=8.0)
    rate = st.selectbox("Hourly Rate", [35, 40, 45, 50, 55, 60, 65])
    labor_cost = calculate_labor_cost(num_laborers, hours, rate)

    # Equipment
    st.markdown("🚜 **Equipment Rental**")
    excavator = st.checkbox("Excavator ($400)")
    skid_steer = st.checkbox("Skid Steer ($350)")
    dump_truck = st.checkbox("Dump Truck ($300)")
    equipment_cost = calculate_equipment_cost(excavator, skid_steer, dump_truck)

    # Travel
    st.markdown("🚗 **Travel Costs**")
    trailer_km = st.number_input("Trailer Transport (km)", min_value=0)
    passenger_km = st.number_input("Passenger Vehicle (km)", min_value=0)
    travel_cost = calculate_travel_cost(trailer_km, passenger_km)

    # Totals
    st.markdown("🧾 **Totals**")
    material_cost = calculate_material_cost(product, sqft, data, margin_decimal)
    lifter_cost = 100 if include_lifter else 0

    subtotal, hst, grand_total = calculate_total(
        material_cost, gravel_cost, fabric_cost, sand_cost,
        lifter_cost, labor_cost, equipment_cost, travel_cost
    )

    st.markdown(f"**📦 Material Cost:** ${material_cost:.2f}")
    st.markdown(f"**🧰 Equipment Cost:** ${equipment_cost:.2f}")
    st.markdown(f"**👷 Labor Cost:** ${labor_cost:.2f}")
    st.markdown(f"**🚗 Travel Cost:** ${travel_cost:.2f}")
    st.markdown(f"**🪨 Gravel:** ${gravel_cost:.2f} | Fabric: ${fabric_cost:.2f} | Sand: ${sand_cost:.2f} | Lifter: ${lifter_cost:.2f}")
    st.markdown(f"**💵 Subtotal:** ${subtotal:.2f} | **HST (15%):** ${hst:.2f}")
    st.markdown(f"### 🧾 Grand Total: **${grand_total:.2f}**")
