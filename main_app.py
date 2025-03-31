import streamlit as st
import pandas as pd
from utils import load_paver_data, calculate_material_cost

st.set_page_config("AKL Hardscape Master Tool", layout="wide")
st.title("🧱 AKL Hardscape Master Tool")
st.header("🚶 Walkway Estimator")

# --- Inputs ---
sqft = st.number_input("📐 Square Feet", min_value=0, step=1)
margin = st.slider("📊 Override Margin %", 0, 100, 30)
paver_data = load_paver_data()

product = st.selectbox("🧱 Choose Product", paver_data["Products"].dropna().unique())

st.markdown("---")
st.subheader("🪨 Gravel Base")

include_gravel = st.checkbox("Include Gravel Base", value=True)
gravel_depth = st.number_input("Gravel Depth (inches)", value=6, step=1)
include_geotextile = st.checkbox("Include Geotextile Fabric ($0.50/sq ft)", value=True)

st.markdown("### 🧪 Polymeric Sand")
include_sand = st.checkbox("Include Polymeric Sand", value=True)

st.markdown("### 🦺 Labor")
num_laborers = st.number_input("Number of Laborers", 1, 10, 2)
laborers = []
for i in range(num_laborers):
    col1, col2 = st.columns(2)
    with col1:
        rate = st.number_input(f"Laborer {i+1} Rate ($/hr)", min_value=0, value=45, step=5)
    with col2:
        hours = st.number_input(f"Laborer {i+1} Hours", min_value=0.0, value=8.0, step=0.5)
    laborers.append(rate * hours)

st.markdown("### 🚚 Equipment Use")
equipments = {
    "Excavator": {},
    "Skid Steer": {},
    "Dump Truck": {}
}
for name in equipments:
    col1, col2 = st.columns(2)
    with col1:
        equipments[name]["hours"] = st.number_input(f"{name} Hours", min_value=0.0, value=0.0, step=1.0)
    with col2:
        equipments[name]["trailer_km"] = st.number_input(f"{name} Trailer Km", min_value=0, value=0, step=1)

st.markdown("### 🚗 Travel")
passenger_km = st.number_input("Round Trip Distance (km)", min_value=0, value=30)
passenger_vehicles = st.number_input("Number of Passenger Vehicles", 0, 5, 1)

# --- Calculation ---
st.markdown("---")
st.subheader("📋 Estimate Summary")

mat = calculate_material_cost(product, sqft, paver_data, margin)

# Gravel base
gravel_total = 0
geo_total = 0
if include_gravel:
    cubic_ft = sqft * (gravel_depth / 12)
    cubic_ft *= 1.25  # buffer
    gravel_yards = math.ceil(cubic_ft / 27)
    gravel_total = gravel_yards * 250  # $250 per 5-ton load

if include_geotextile:
    geo_total = sqft * 0.50

# Sand
sand_total = 0
if include_sand:
    bags = math.ceil(sqft / 80)
    sand_total = bags * 60  # $60/bag (adjust as needed)

# Labor
labor_total = sum(laborers)

# Equipment
equip_total = 0
for eq in equipments.values():
    equip_total += eq["hours"] * 130
    # Trailer transport: $250 for first 30 km
    km = eq["trailer_km"]
    if km > 0:
        if km <= 30:
            equip_total += 250
        else:
            equip_total += 250 + ((km - 30) * 4.2)

# Travel
travel_total = passenger_km * passenger_vehicles * 0.80

# Totals
subtotal = mat["total"] + gravel_total + geo_total + sand_total + labor_total + equip_total + travel_total
hst = subtotal * 0.15
grand_total = subtotal + hst

# --- Display ---
st.markdown(f"**Product:** {product}")
st.markdown(f"**Price per Unit (with margin):** ${mat['unit_price_with_margin']:.2f}")
st.markdown(f"**Units Required:** {mat['units']}")
st.markdown(f"**Material Total:** ${mat['total']:.2f}")
if include_gravel:
    st.markdown(f"**Gravel Base:** ${gravel_total:.2f}")
if include_geotextile:
    st.markdown(f"**Geotextile Fabric:** ${geo_total:.2f}")
if include_sand:
    st.markdown(f"**Polymeric Sand:** ${sand_total:.2f}")
st.markdown(f"**Labor Total:** ${labor_total:.2f}")
st.markdown(f"**Equipment Total:** ${equip_total:.2f}")
st.markdown(f"**Travel (Passenger Vehicles):** ${travel_total:.2f}")
st.markdown(f"**Subtotal:** ${subtotal:.2f}")
st.markdown(f"**HST (15%):** ${hst:.2f}")
st.markdown(f"### 💰 Grand Total: ${grand_total:.2f}")
