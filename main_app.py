import streamlit as st
import math
from utils import (
    load_paver_data,
    calculate_material_cost
)

st.set_page_config(page_title="AKL Hardscape Master Tool", layout="wide")

st.title("🧱 AKL Hardscape Master Tool")

section = st.sidebar.radio("📂 Select Project Section", ["Walkway", "Retaining Wall", "Steps", "Fire Pit", "🧾 Quote Preview"])

if section == "Walkway":
    st.header("🚶‍♂️ Walkway Estimator")

    sqft = st.number_input("📏 Square Feet", min_value=0)
    margin_override = st.slider("📊 Override Margin %", 0, 100, 30)

    paver_data = load_paver_data()
    product_name = st.selectbox("🧱 Choose Product", paver_data["Products"].dropna().unique())

    # Gravel Section
    st.subheader("🪨 Gravel")
    include_gravel = st.checkbox("✅ Include Gravel Base", value=True)
    gravel_depth = st.number_input("Gravel Depth (inches)", min_value=0, value=6)
    include_geotextile = st.checkbox("📏 Include Geotextile Fabric ($0.50/sq ft)", value=True)

    # Polymeric Sand
    st.subheader("🧪 Polymeric Sand")
    sand_type = st.selectbox("Choose Paver Type", ["Pavers", "Square Cut Flagstone", "Random Flagstone"])
    if sand_type == "Pavers":
        sand_coverage = 80
    elif sand_type == "Square Cut Flagstone":
        sand_coverage = 120
    else:
        sand_coverage = 50

    # Labor Section
    st.subheader("👷 Labor")
    num_laborers = st.number_input("Number of Laborers", min_value=1, max_value=10, value=1)
    labor_inputs = []
    for i in range(num_laborers):
        col1, col2 = st.columns(2)
        with col1:
            pay_rate = st.number_input(f"Laborer {i+1} Pay Rate ($/hr)", min_value=0, value=35)
        with col2:
            hours = st.number_input(f"Laborer {i+1} Hours", min_value=0, value=8)
        labor_inputs.append((pay_rate, hours))

    # Equipment Section
    st.subheader("🚜 Equipment Use")
    equipment = {
        "Excavator": {},
        "Skid Steer": {},
        "Dump Truck": {}
    }
    for name in equipment:
        col1, col2 = st.columns(2)
        with col1:
            equipment[name]["hours"] = st.number_input(f"{name} Hours", min_value=0, value=0)
        with col2:
            equipment[name]["trailer_km"] = st.number_input(f"{name} Trailer Km", min_value=0, value=0)

    # Travel Section
    st.subheader("🚗 Passenger Travel")
    passenger_km = st.number_input("Round Trip Distance (km)", min_value=0, value=35)
    num_vehicles = st.number_input("Number of Passenger Vehicles", min_value=1, value=1)

    # Material Cost
    material_cost, units = calculate_material_cost(product_name, sqft, paver_data, margin_override)

    # Gravel Calculation
    gravel_cost = 0
    if include_gravel:
        cubic_feet = sqft * (gravel_depth / 12) * 1.25
        cubic_yards = cubic_feet / 27
        loads_needed = math.ceil(cubic_yards / 3)
        gravel_cost = loads_needed * 250 * 1.15

    # Geotextile Fabric
    fabric_cost = sqft * 0.50 * 1.15 if include_geotextile else 0

    # Polymeric Sand
    sand_bags = math.ceil(sqft / sand_coverage)
    sand_cost = sand_bags * 75 * 1.15

    # Labor Total
    labor_total = sum([math.ceil(rate * hrs) for rate, hrs in labor_inputs]) * 1.15

    # Equipment Total
    equip_total = 0
    trailer_km_total = 0
    for machine, data in equipment.items():
        equip_hours = data["hours"]
        trailer_km = data["trailer_km"]
        trailer_km_total += trailer_km
        equip_total += equip_hours * 130 * 1.15

    # Trailer Transport Fee
    trailer_cost = 250 if trailer_km_total <= 30 else 250 + ((trailer_km_total - 30) * 4.20)
    trailer_cost *= 1.15

    # Passenger Travel
    passenger_cost = passenger_km * 0.80 * num_vehicles * 1.15

    # Final Total
    total = sum([
        material_cost,
        gravel_cost,
        fabric_cost,
        sand_cost,
        labor_total,
        equip_total,
        trailer_cost,
        passenger_cost
    ])

    st.subheader("📊 Estimate Summary")
    st.write(f"🧱 Material Cost ({units} units): ${material_cost:,.2f}")
    st.write(f"🪨 Gravel Base: ${gravel_cost:,.2f}")
    st.write(f"🧵 Geotextile Fabric: ${fabric_cost:,.2f}")
    st.write(f"🧪 Polymeric Sand: ${sand_cost:,.2f}")
    st.write(f"👷 Labor Total: ${labor_total:,.2f}")
    st.write(f"🚜 Equipment Total: ${equip_total:,.2f}")
    st.write(f"🚛 Trailer Transport: ${trailer_cost:,.2f}")
    st.write(f"🚗 Passenger Vehicle Travel: ${passenger_cost:,.2f}")
    st.markdown("---")
    st.write(f"💵 **Total (with 15% HST): ${total:,.2f}**")
