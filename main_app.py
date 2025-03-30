import streamlit as st
from utils import (
    load_paver_data,
    calculate_material_cost,
)
import math

st.set_page_config(page_title="AKL Hardscape Master Tool", layout="wide")

st.title("🧱 AKL Hardscape Master Tool")

# Sidebar navigation
section = st.sidebar.radio("📂 Select Project Section", ["Walkway", "Retaining Wall", "Steps", "Fire Pit", "Quote Preview"])

if section == "Walkway":
    st.header("🚶‍♂️ Walkway Estimator")

    sqft = st.number_input("📏 Square Feet", min_value=0, value=0)

    margin_override = st.slider("📊 Override Margin %", 0, 100, 30)

    data = load_paver_data()
    products = data["Products"].dropna().unique()
    selected_product = st.selectbox("🧱 Choose Product", options=products)

    # Material cost
    material_cost = calculate_material_cost(selected_product, sqft, data, margin_override)

    # Optional gravel
    include_gravel = st.checkbox("🪨 Include Gravel Base", value=True)
    gravel_depth = st.number_input("Gravel Depth (inches)", value=6, step=1) if include_gravel else 0
    include_fabric = st.checkbox("📄 Include Geotextile Fabric ($0.50/sq ft)", value=True) if include_gravel else False

    gravel_area = sqft * 1.25 if include_gravel else 0
    gravel_volume = gravel_area * (gravel_depth / 12)  # in cubic feet
    gravel_yds = gravel_volume / 27
    gravel_loads = math.ceil(gravel_yds / 3)
    gravel_cost = gravel_loads * 250 if include_gravel else 0
    fabric_cost = sqft * 0.50 if include_gravel and include_fabric else 0

    # Polymeric sand
    st.subheader("🧪 Polymeric Sand")
    sand_bags = math.ceil(sqft / 80)
    sand_cost = sand_bags * 35

    # Labor inputs
    st.subheader("👷‍♂️ Labor")
    num_laborers = st.number_input("Number of Laborers", min_value=1, max_value=10, value=2)
    laborers = []
    for i in range(num_laborers):
        col1, col2 = st.columns(2)
        with col1:
            rate = st.number_input(f"Laborer {i+1} - $/hr", value=40, key=f"rate_{i}")
        with col2:
            hours = st.number_input(f"Laborer {i+1} - Hours", value=8, step=1, key=f"hours_{i}")
        laborers.append(rate * hours)

    labor_cost = sum(laborers)

    # Equipment
    st.subheader("🚜 Equipment Use")
    equipment = {
        "Excavator": {},
        "Skid Steer": {},
        "Dump Truck": {}
    }

    for machine in equipment.keys():
        equipment[machine]["Hours"] = st.number_input(f"{machine} Hours", min_value=0, step=1, value=0, key=f"{machine}_hours")
        equipment[machine]["Km"] = st.number_input(f"{machine} Trailer Km", min_value=0, step=1, value=0, key=f"{machine}_km")

    equipment_cost = 0
    for machine, values in equipment.items():
        hours = values["Hours"]
        km = values["Km"]
        hourly = 130
        trailer_base = 250
        trailer_km_cost = max(km - 30, 0) * 4.20 if km > 30 else 0
        trailer_total = trailer_base + trailer_km_cost if km > 0 else 0
        equipment_cost += (hours * hourly) + trailer_total

    # Passenger vehicle travel
    st.subheader("🚗 Passenger Travel")
    round_trip_km = st.number_input("Round Trip Distance (km)", value=0, step=1)
    num_pass_vehicles = st.number_input("Number of Passenger Vehicles", value=1, min_value=0, step=1)
    passenger_travel_cost = round_trip_km * 0.80 * num_pass_vehicles

    # Totals
    st.subheader("📦 Summary")
    subtotal = material_cost + gravel_cost + fabric_cost + sand_cost + labor_cost + equipment_cost + passenger_travel_cost
    tax = subtotal * 0.15
    total = subtotal + tax

    st.write(f"**Material Cost:** ${material_cost:,.2f}")
    if include_gravel:
        st.write(f"**Gravel Loads:** {gravel_loads} @ $250 each = ${gravel_cost:,.2f}")
        if include_fabric:
            st.write(f"**Geotextile Fabric:** ${fabric_cost:,.2f}")
    st.write(f"**Polymeric Sand:** {sand_bags} bags = ${sand_cost:,.2f}")
    st.write(f"**Labor:** ${labor_cost:,.2f}")
    st.write(f"**Equipment:** ${equipment_cost:,.2f}")
    st.write(f"**Passenger Travel:** ${passenger_travel_cost:,.2f}")
    st.write("---")
    st.write(f"**Subtotal:** ${subtotal:,.2f}")
    st.write(f"**HST (15%):** ${tax:,.2f}")
    st.success(f"**Total: ${total:,.2f}**")
