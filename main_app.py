import streamlit as st
import pandas as pd
import math
from utils import load_paver_data, calculate_material_cost

# Constants
TAX_RATE = 0.15
EDGE_RESTRAINT_COST = 220
INLAY_COST = 4000
GRAVEL_COST_PER_LOAD = 250
TRAVEL_COST_PER_KM = 4.20
PASSENGER_COST_PER_KM = 0.80
EQUIPMENT_HOURLY_RATE = 130

# App Config
st.set_page_config(page_title="AKL Hardscape Master Tool", layout="wide")
st.markdown("## 🧱 AKL Hardscape Master Tool")
st.markdown("### 🧍‍♂️ Walkway Estimator")

try:
    df = load_paver_data()

    sqft = st.number_input("📏 Square Feet", min_value=0, step=1)
    margin = st.slider("📊 Override Margin %", 0, 100, 30)
    product = st.selectbox("🧱 Choose Product", df["Products"].dropna().unique())

    # Labor
    st.markdown("### 👷 Labor")
    num_laborers = st.selectbox("Number of Laborers", [1, 2, 3], index=1)
    labor_total = 0
    for i in range(num_laborers):
        hours = st.selectbox(f"Hours for Laborer #{i+1}", options=list(range(1, 13)), key=f"h{i}")
        rate = st.selectbox(f"Hourly Rate for Laborer #{i+1}", [35, 40, 45, 50, 55, 60, 65], key=f"r{i}")
        labor_total += hours * rate

    # Equipment
    st.markdown("### 🚜 Equipment Use")
    excavator_hours = st.selectbox("Excavator Hours", list(range(0, 13)), index=1)
    skid_steer_hours = st.selectbox("Skid Steer Hours", list(range(0, 13)), index=0)
    dump_truck_hours = st.selectbox("Dump Truck Hours", list(range(0, 13)), index=0)
    excavator_km = st.number_input("Excavator Trailer Km", min_value=0, step=1)
    skid_km = st.number_input("Skid Steer Trailer Km", min_value=0, step=1)
    truck_km = st.number_input("Dump Truck Trailer Km", min_value=0, step=1)

    # Travel
    st.markdown("### 🚗 Travel")
    round_trip_km = st.number_input("Round Trip Distance (km)", min_value=0, step=1, value=30)
    passenger_vehicles = st.selectbox("Number of Passenger Vehicles", [1, 2, 3], index=0)

    # Add-ons
    st.markdown("### ➕ Add-Ons")
    inlay = st.checkbox("Include 4 ft wide inlay ($4000 + HST)")
    sand_type = st.selectbox("Polymeric Sand Type", ["None", "$50+tax per bag", "$75+tax per bag"])
    gravel_addon_loads = st.selectbox("Extra Gravel Loads", list(range(0, 6)), index=0)
    gravel_price_input = st.number_input("Extra Gravel Price per Load ($)", value=250, step=1)
    gravel_delivery_km = st.number_input("Delivery Distance (km)", value=30, step=1)

    # Calculations
    material = calculate_material_cost(product, sqft, df, margin_override=margin)
    gravel_yards = math.ceil((sqft * 0.5) / 27)
    gravel_base_cost = gravel_yards * GRAVEL_COST_PER_LOAD

    edge_units = math.ceil(sqft / 100)
    edge_cost = edge_units * EDGE_RESTRAINT_COST * (1 + TAX_RATE)

    inlay_cost = INLAY_COST * (1 + TAX_RATE) if inlay else 0

    sand_cost = 0
    if sand_type == "$50+tax per bag":
        coverage = 80
        bag_price = 50
    elif sand_type == "$75+tax per bag":
        coverage = 80
        bag_price = 75
    else:
        coverage = 0
        bag_price = 0

    if coverage:
        sand_bags = math.ceil(sqft / coverage)
        sand_cost = sand_bags * bag_price * (1 + TAX_RATE)

    extra_km = max(0, gravel_delivery_km - 30)
    gravel_addon_cost = gravel_addon_loads * gravel_price_input + (extra_km * TRAVEL_COST_PER_KM)

    equipment_total = (excavator_hours + skid_steer_hours + dump_truck_hours) * EQUIPMENT_HOURLY_RATE * (1 + TAX_RATE)

    trailer_cost = 0
    for km in [excavator_km, skid_km, truck_km]:
        trailer_cost += 250 if km <= 30 else 250 + (km - 30) * TRAVEL_COST_PER_KM

    trailer_cost *= (1 + TAX_RATE)

    passenger_travel = round_trip_km * passenger_vehicles * PASSENGER_COST_PER_KM

    # Totals
    subtotal = (
        material["material_total"] + gravel_base_cost + edge_cost +
        labor_total + equipment_total + trailer_cost + passenger_travel +
        gravel_addon_cost + sand_cost + inlay_cost
    )
    hst = subtotal * TAX_RATE
    final = subtotal + hst

    # Display
    st.markdown("## 📋 Estimate Summary")
    st.write(f"**Product:** {product}")
    st.write(f"**Price per Unit (with margin):** ${material['unit_price']}")
    st.write(f"**Units Required:** {material['units_required']}")
    st.write(f"**Material Total:** ${material['material_total']}")
    st.markdown("---")
    st.write(f"**Gravel Yards:** {gravel_yards} @ 250/yd = ${gravel_base_cost}")
    st.write(f"**Edge Restraint:** {edge_units} x $220 = ${round(edge_cost,2)}")
    st.write(f"**Labor Total:** ${round(labor_total, 2)}")
    st.write(f"**Equipment Cost:** ${round(equipment_total, 2)}")
    st.write(f"**Trailer Transport:** ${round(trailer_cost, 2)}")
    st.write(f"**Passenger Vehicle Travel:** ${round(passenger_travel, 2)}")
    st.write(f"**Extra Gravel Loads:** ${round(gravel_addon_cost, 2)}")
    if sand_cost:
        st.write(f"**Polymeric Sand:** ${round(sand_cost, 2)}")
    if inlay_cost:
        st.write(f"**Inlay Add-On:** ${round(inlay_cost, 2)}")
    st.markdown("---")
    st.write(f"**Subtotal:** ${round(subtotal, 2)}")
    st.write(f"**HST (15%):** ${round(hst, 2)}")
    st.markdown(f"### 💰 Final Total: ${round(final, 2)}")

except Exception as e:
    st.error(f"Something went wrong: {e}")
