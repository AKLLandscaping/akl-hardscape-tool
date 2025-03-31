import streamlit as st
import math
from utils import load_paver_data, calculate_material_cost

# Constants
EDGE_RESTRAINT_COST = 220
INLAY_COST_FULL = 4000
INLAY_COST_SIMPLE = 2850
GRAVEL_COST_PER_LOAD = 250
SAND_COST_PER_BAG = 50  # Will be updated by dropdown
EQUIPMENT_HOURLY_RATE = 130
TRAVEL_COST_PER_KM = 4.20
PASSENGER_TRAVEL_COST_PER_KM = 0.80
TAX_RATE = 0.15
FOOD_COST_PER_LABORER = 50

st.set_page_config(page_title="AKL Hardscape Master Tool – Walkway Estimator", layout="wide")
st.markdown("## 🧱 AKL Hardscape Master Tool – Walkway Estimator")

try:
    df = load_paver_data()

    # 📐 Inputs
    sqft = st.number_input("📏 Square Feet", min_value=0, value=100, step=1)
    margin = st.slider("📊 Override Margin %", 0, 100, 30)

    # 🧱 Material
    products = df["Products"].dropna().unique()
    product = st.selectbox("Choose Product", products)
    selected_row = df[df["Products"] == product].iloc[0]
    unit_type = selected_row["Unit"]
    coverage = selected_row["Coverage"]
    net_price = selected_row["Net"]
    unit_price = net_price * (1 + margin / 100)
    units_required = math.ceil(sqft / coverage) if unit_type == "sft" else 1
    material_total = round(units_required * unit_price, 2)

    # 🦺 Labor
    st.subheader("👷 Labor")
    num_laborers = st.selectbox("Number of Laborers", list(range(1, 11)), index=1)
    labor_total = 0
    for i in range(num_laborers):
        hours = st.selectbox(f"Hours for Laborer #{i+1}", list(range(1, 13)), key=f"hours_{i}")
        rate = st.selectbox(f"Hourly Rate for Laborer #{i+1}", [35, 40, 45, 50, 55, 60, 65], key=f"rate_{i}")
        labor_total += hours * rate

    # 🚜 Equipment
    st.subheader("🚜 Equipment Use")
    excavator_hours = st.selectbox("Excavator Hours", list(range(0, 13)))
    skid_steer_hours = st.selectbox("Skid Steer Hours", list(range(0, 13)))
    dump_truck_hours = st.selectbox("Dump Truck Hours", list(range(0, 13)))

    excavator_km = st.number_input("Excavator Trailer Km", min_value=0, value=30, step=1)
    skid_km = st.number_input("Skid Steer Trailer Km", min_value=0, value=30, step=1)
    truck_km = st.number_input("Dump Truck Trailer Km", min_value=0, value=30, step=1)

    equipment_cost = (excavator_hours + skid_steer_hours + dump_truck_hours) * EQUIPMENT_HOURLY_RATE
    trailer_cost = sum(
        250 if km <= 30 else 250 + (km - 30) * TRAVEL_COST_PER_KM
        for km in [excavator_km, skid_km, truck_km]
    )

    # 🚗 Travel
    st.subheader("🚗 Travel")
    round_trip_km = st.number_input("Round Trip Distance (km)", min_value=0, value=30, step=1)
    passenger_vehicles = st.selectbox("Number of Passenger Vehicles", list(range(1, 11)))
    passenger_travel_cost = round_trip_km * PASSENGER_TRAVEL_COST_PER_KM * passenger_vehicles

    # ➕ Add-Ons
    st.subheader("➕ Add-Ons")
    inlay_full = st.checkbox("Include 4 ft wide inlay ($4000 + HST)")
    inlay_simple = st.checkbox("Inlay w/ no background or border ($2850 + HST)")
    inlay_total = 0
    if inlay_full:
        inlay_total += round(INLAY_COST_FULL * (1 + TAX_RATE), 2)
    if inlay_simple:
        inlay_total += round(INLAY_COST_SIMPLE * (1 + TAX_RATE), 2)

    sand_type = st.selectbox("Polymeric Sand Type", ["None", "$50+tax per bag", "$75+tax per bag"])
    sand_price = 50 if "50" in sand_type else 75 if "75" in sand_type else 0
    sand_bags = 0
    if sand_price:
        sand_bags = math.ceil(sqft / 80)
    sand_total = sand_bags * sand_price * (1 + TAX_RATE)

    extra_gravel_loads = st.selectbox("Extra Gravel Loads", list(range(0, 6)), index=0)
    extra_gravel_price = st.number_input("Extra Gravel Price per Load ($)", value=250, step=1)
    extra_gravel_km = st.number_input("Delivery Distance (km)", value=30, step=1)
    extra_km_charge = max(0, extra_gravel_km - 30) * TRAVEL_COST_PER_KM
    extra_gravel_total = extra_gravel_loads * extra_gravel_price + extra_km_charge

    # 🛏️ Overnight Stay
    st.subheader("🛏️ Overnight Stay")
    overnight_room_cost = st.number_input("Room Cost ($)", min_value=0, step=1)
    overnight_laborers = st.selectbox("Number of Laborers Staying Overnight", list(range(0, 11)), index=0)
    overnight_food_total = overnight_laborers * FOOD_COST_PER_LABORER * (1 + TAX_RATE)
    overnight_total = overnight_room_cost + overnight_food_total

    # 🪨 Gravel Base
    gravel_yards = math.ceil(sqft * 0.5 / 27)
    gravel_base_total = gravel_yards * GRAVEL_COST_PER_LOAD

    # 📋 Estimate Summary
    st.subheader("📋 Estimate Summary")
    st.write(f"**Product:** {product} ({unit_type})")
    st.write(f"**Price per Unit (with margin):** ${round(unit_price, 2)}")
    st.write(f"**Units Required:** {units_required}")
    st.write(f"**Material Total:** ${material_total}")
    st.markdown("---")
    st.write(f"**Gravel Yards:** {gravel_yards} @ $250/yd = ${gravel_base_total}")
    st.write(f"**Edge Restraint:** {math.ceil(sqft / 100)} x $220 = ${math.ceil(sqft / 100) * EDGE_RESTRAINT_COST * (1 + TAX_RATE):.2f}")
    st.write(f"**Labor Total:** ${labor_total:.2f}")
    st.write(f"**Equipment Cost:** ${equipment_cost:.2f}")
    st.write(f"**Trailer Transport:** ${trailer_cost:.2f}")
    st.write(f"**Passenger Vehicle Travel:** ${passenger_travel_cost:.2f}")
    if extra_gravel_loads > 0:
        st.write(f"**Extra Gravel Loads:** ${extra_gravel_total:.2f}")
    if sand_bags > 0:
        st.write(f"**Polymeric Sand:** {sand_bags} bags = ${sand_total:.2f}")
    if inlay_total > 0:
        st.write(f"**Inlay Add-On:** ${inlay_total:.2f}")
    if overnight_total > 0:
        st.write(f"**Overnight Stay Total:** ${overnight_total:.2f}")

    # 🧾 Totals
    subtotal = (
        material_total + gravel_base_total +
        (math.ceil(sqft / 100) * EDGE_RESTRAINT_COST * (1 + TAX_RATE)) +
        labor_total + equipment_cost + trailer_cost +
        passenger_travel_cost + extra_gravel_total + sand_total +
        inlay_total + overnight_total
    )
    hst = round(subtotal * TAX_RATE, 2)
    final = round(subtotal + hst, 2)

    st.markdown("---")
    st.write(f"**Subtotal:** ${round(subtotal, 2)}")
    st.write(f"**HST (15%):** ${hst}")
    st.markdown(f"### 💰 Final Total: ${final}")

except Exception as e:
    st.error(f"Something went wrong: {e}")
