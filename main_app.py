import streamlit as st
import math
import pandas as pd
from utils import load_paver_data, calculate_material_cost

# === CONSTANTS ===
EDGE_RESTRAINT_COST = 220  # per 100 sq ft
INLAY_COST = 4000
BASE_GRAVEL_COST = 250
TRAVEL_RATE = 4.20
TRAVEL_INCLUDED_KM = 30
HST = 0.15
PASSENGER_VEHICLE_COST = 0.80
SAND_COST_OPTIONS = {"$50+tax per bag": 50, "$75+tax per bag": 75}

# === STREAMLIT CONFIG ===
st.set_page_config("AKL Hardscape Master Tool", layout="wide")
st.title("🧱 AKL Hardscape Master Tool")
st.header("🧍‍♂️ Walkway Estimator")

# === LOAD DATA ===
df = load_paver_data()
products = df["Products"].dropna().unique()

# === USER INPUTS ===
sqft = st.number_input("📏 Square Feet", min_value=0, step=1)
margin = st.slider("📉 Override Margin %", 0, 100, 30)
product = st.selectbox("🧱 Choose Product", options=products)

# === LABOR ===
st.subheader("👷 Labor")
num_laborers = st.selectbox("Number of Laborers", options=[1, 2, 3])
labor_total = 0
for i in range(num_laborers):
    hours = st.selectbox(f"Hours for Laborer #{i+1}", options=list(range(1, 13)), key=f"hours_{i}")
    rate = st.selectbox(f"Hourly Rate for Laborer #{i+1}", options=[35, 40, 45, 50, 55, 60, 65], key=f"rate_{i}")
    labor_total += hours * rate

# === EQUIPMENT ===
st.subheader("🚜 Equipment Use")
excavator_hours = st.selectbox("Excavator Hours", list(range(0, 13)), index=0)
skid_hours = st.selectbox("Skid Steer Hours", list(range(0, 13)), index=0)
dump_hours = st.selectbox("Dump Truck Hours", list(range(0, 13)), index=0)
equipment_total = (excavator_hours + skid_hours + dump_hours) * 130

# === TRAILER TRAVEL ===
excavator_km = st.number_input("Excavator Trailer Km", value=0, step=1)
skid_km = st.number_input("Skid Steer Trailer Km", value=0, step=1)
dump_km = st.number_input("Dump Truck Trailer Km", value=0, step=1)
def trailer_cost(km):
    return 250 if km <= TRAVEL_INCLUDED_KM else 250 + ((km - TRAVEL_INCLUDED_KM) * TRAVEL_RATE)
trailer_total = trailer_cost(excavator_km) + trailer_cost(skid_km) + trailer_cost(dump_km)

# === PASSENGER VEHICLE ===
st.subheader("🚗 Travel")
round_trip_km = st.number_input("Round Trip Distance (km)", value=0, step=1)
num_passenger_vehicles = st.selectbox("Number of Passenger Vehicles", options=list(range(1, 6)))
passenger_cost = round_trip_km * PASSENGER_VEHICLE_COST * num_passenger_vehicles

# === ADD-ONS ===
st.subheader("➕ Add-Ons")
inlay = st.checkbox("Include 4 ft wide inlay ($4000 + HST)")
sand_type = st.selectbox("Polymeric Sand Type", options=list(SAND_COST_OPTIONS.keys()))

# Gravel addon
addon_gravel_loads = st.selectbox("Extra Gravel Loads", list(range(0, 11)))
addon_gravel_price = st.number_input("Extra Gravel Price per Load ($)", value=250)
addon_gravel_km = st.number_input("Delivery Distance (km)", value=30, step=1)
extra_km = max(0, addon_gravel_km - 30)
gravel_addon_total = addon_gravel_loads * addon_gravel_price + extra_km * 4.20

# === CALCULATIONS ===
material = calculate_material_cost(product, sqft, df, margin)
gravel_yards = math.ceil((sqft * 0.5) / 27)
gravel_base_total = gravel_yards * BASE_GRAVEL_COST
edge_units = math.ceil(sqft / 100)
edge_total = edge_units * EDGE_RESTRAINT_COST
inlay_total = INLAY_COST if inlay else 0
sand_cost = 0
if sand_type != "None":
    bag_cost = SAND_COST_OPTIONS[sand_type]
    bags_needed = math.ceil(sqft / 80)  # Assuming average 80 sq ft per bag
    sand_cost = bags_needed * bag_cost

# === TOTALS ===
subtotal = sum([
    material["material_total"],
    gravel_base_total,
    edge_total,
    inlay_total,
    sand_cost,
    labor_total,
    equipment_total,
    trailer_total,
    passenger_cost,
    gravel_addon_total
])
hst_amount = subtotal * HST
final_total = subtotal + hst_amount

# === SUMMARY ===
st.subheader("📋 Estimate Summary")
st.write(f"**Product:** {product}")
st.write(f"**Price per Unit (with margin):** ${material['unit_price']}")
st.write(f"**Units Required:** {material['units_required']}")
st.write(f"**Material Total:** ${material['material_total']}")
st.markdown("---")
st.write(f"Gravel Yards: {gravel_yards} @ 250/yd = ${gravel_base_total}")
st.write(f"Edge Restraint: {edge_units} x $220 = ${edge_total}")
if inlay:
    st.write(f"Inlay Add-On: ${inlay_total}")
if sand_type != "None":
    st.write(f"Polymeric Sand: {bags_needed} bags x ${bag_cost} = ${sand_cost}")
st.write(f"Labor Total: ${labor_total}")
st.write(f"Equipment Total: ${equipment_total}")
st.write(f"Trailer Transport: ${trailer_total}")
st.write(f"Passenger Vehicle Travel: ${passenger_cost}")
if gravel_addon_total > 0:
    st.write(f"Extra Gravel Loads: ${gravel_addon_total}")
st.markdown("---")
st.write(f"**Subtotal:** ${round(subtotal, 2)}")
st.write(f"**HST (15%):** ${round(hst_amount, 2)}")
st.markdown(f"### 💰 Final Total: ${round(final_total, 2)}")
