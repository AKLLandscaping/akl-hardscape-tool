import streamlit as st
from utils import (
    load_paver_data, load_wall_data, load_steps_data,
    load_firepit_data, load_garden_wall_data, load_extras_data,
    calculate_material_cost, calculate_gravel_cost, calculate_fabric_cost,
    calculate_polymeric_sand, calculate_labor_cost, calculate_equipment_cost,
    calculate_travel_cost, calculate_total
)

st.set_page_config(page_title="AKL Hardscape Master Tool", layout="centered")
st.title("🧱 AKL Hardscape Master Tool")

section = st.radio("📂 Select Project Section", ["Walkway", "Retaining Wall", "Steps", "Fire Pit", "Quote Preview"])

paver_data = load_paver_data()
wall_data = load_wall_data()
steps_data = load_steps_data()
firepit_data = load_firepit_data()
garden_wall_data = load_garden_wall_data()
extras_data = load_extras_data()

def walkway_calculator():
    st.header("🚶‍♂️ Walkway Calculator")
    product = st.selectbox("Choose Material", paver_data[paver_data.columns[1]].dropna().unique())
    sqft = st.number_input("Square Feet", min_value=0.0)

    if sqft:
        mat_cost = calculate_material_cost(product, sqft, paver_data)

        include_gravel = st.checkbox("Include Gravel Base", value=True)
        gravel_depth = st.number_input("Gravel Depth (inches)", value=6.0)
        gravel_cost, gravel_volume, gravel_loads = (0, 0, 0)
        if include_gravel:
            gravel_cost, gravel_volume, gravel_loads = calculate_gravel_cost(sqft, gravel_depth)
            st.markdown(f"Gravel Volume: {gravel_volume} yd³ → Loads: {gravel_loads}, Cost: ${gravel_cost:.2f}")

        include_fabric = st.checkbox("Include Geotextile Fabric ($0.50/sq ft)", value=True)
        fabric_cost = calculate_fabric_cost(sqft) if include_fabric else 0

        bags, sand_cost = calculate_polymeric_sand(sqft, product)
        st.markdown(f"🧱 Polymeric Sand: {bags} bags needed → ${sand_cost:.2f}")

        labor_rate = st.slider("Labor Rate ($/hr)", 35, 65, 50)
        labor_hours = st.slider("Total Labor Hours", 1, 20, 8)
        labor_cost = calculate_labor_cost(1, labor_hours, labor_rate)

        st.markdown("### Equipment")
        excavator = st.checkbox("Excavator ($400)")
        skid_steer = st.checkbox("Skid Steer ($350)")
        dump_truck = st.checkbox("Dump Truck ($300)")
        equipment_cost = calculate_equipment_cost(excavator, skid_steer, dump_truck)

        trailer_km = st.number_input("Trailer Travel (km)", 0)
        passenger_km = st.number_input("Passenger Vehicle Travel (km)", 0)
        travel_cost = calculate_travel_cost(trailer_km, passenger_km)

        subtotal, hst, total = calculate_total(
            mat_cost, gravel_cost, fabric_cost, sand_cost,
            labor_cost, equipment_cost, travel_cost
        )

        st.markdown(f"### ✅ Total Cost: ${subtotal:.2f} + HST (${hst:.2f}) = ${total:.2f}")

if section == "Walkway":
    walkway_calculator()
