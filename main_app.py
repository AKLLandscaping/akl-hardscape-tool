import streamlit as st
from utils import (
    load_paver_data,
    load_wall_data,
    load_steps_data,
    load_firepit_data,
    load_garden_wall_data,
    calculate_material_cost,
    calculate_gravel_cost,
    calculate_fabric_cost,
    calculate_polymeric_sand,
    calculate_labor_cost,
    calculate_equipment_cost,
    calculate_travel_cost,
    calculate_total
)

st.set_page_config(page_title="AKL Hardscape Master Tool", layout="wide")
st.title("🧱 AKL Hardscape Master Tool")

# --- SECTION SELECTOR ---
section = st.sidebar.radio("📂 Select Project Section", [
    "Walkway", "Retaining Wall", "Steps", "Fire Pit"
])

# --- MARGIN PERCENT OVERRIDE ---
margin_override = st.sidebar.slider("📈 Override Margin %", min_value=0, max_value=100, value=30)

# --- LOAD PRODUCT DATA ---
if section == "Walkway":
    data = load_paver_data()
elif section == "Retaining Wall":
    data = load_wall_data()
elif section == "Steps":
    data = load_steps_data()
elif section == "Fire Pit":
    data = load_firepit_data()
else:
    data = load_paver_data()

product_names = data["Product Name"].dropna().unique()
product_name = st.selectbox("🧱 Select Product", product_names)

# --- INPUTS ---
sqft = st.number_input("📏 Square Feet (or total units)", min_value=0.0, value=100.0)
depth = st.number_input("📐 Gravel Depth (inches)", min_value=0.0, value=6.0)

st.markdown("### 👷 Labor")
num_laborers = st.number_input("Laborers", min_value=0, value=1)
labor_total = 0
for i in range(num_laborers):
    rate = st.number_input(f"Laborer {i+1} Rate ($/hr)", min_value=0.0, value=55.0)
    hours = st.number_input(f"Laborer {i+1} Hours", min_value=0.0, value=8.0)
    labor_total += calculate_labor_cost(1, hours, rate)

st.markdown("### 🚜 Equipment")
excavator = st.checkbox("Excavator ($400/day)")
skid_steer = st.checkbox("Skid Steer ($350/day)")
dump_truck = st.checkbox("Dump Truck ($300/day)")

st.markdown("### 🚚 Travel")
trailer_km = st.number_input("Trailer Travel (km)", min_value=0.0, value=0.0)
passenger_km = st.number_input("Passenger Vehicle Travel (km)", min_value=0.0, value=0.0)

# --- CALCULATIONS ---
material_cost = calculate_material_cost(product_name, sqft, data, margin_override)
gravel_cost, gravel_vol, gravel_loads = calculate_gravel_cost(sqft, depth)
fabric_cost = calculate_fabric_cost(sqft)
bags, sand_cost = calculate_polymeric_sand(sqft, product_name)
equipment_cost = calculate_equipment_cost(excavator, skid_steer, dump_truck)
travel_cost = calculate_travel_cost(trailer_km, passenger_km)

# --- TOTALS ---
subtotal, hst, grand_total = calculate_total(
    material_cost, gravel_cost, fabric_cost,
    sand_cost, labor_total, equipment_cost, travel_cost
)

# --- DISPLAY ---
st.markdown("## 💰 Quote Summary")
st.write(f"**Material Cost:** ${material_cost}")
st.write(f"**Gravel Cost:** ${gravel_cost} ({gravel_loads} loads, {gravel_vol:.2f} yd³)")
st.write(f"**Fabric Cost:** ${fabric_cost}")
st.write(f"
