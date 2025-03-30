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

st.set_page_config(page_title="AKL Hardscape Tool", layout="wide")
st.title("🧱 AKL Hardscape Master Tool")

# Section selector
section = st.sidebar.radio("📂 Select Project Section", ["Walkway", "Retaining Wall", "Steps", "Fire Pit"])

# Load corresponding data
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

# Filter data to valid products
material_options = data["Product Name"].dropna().unique()
selected_material = st.selectbox("🧱 Select Material", material_options)

# Shared inputs
st.subheader("📐 Job Details")
sqft = st.number_input("Enter square footage (or # units for EA)", min_value=0.0, value=100.0)
depth = st.number_input("Gravel Base Depth (inches)", min_value=0.0, value=6.0)
margin = st.slider("📈 Apply Margin %", min_value=0, max_value=100, value=30)

# Labor
st.subheader("👷 Labor")
num_laborers = st.number_input("Number of Laborers", min_value=0, value=1)
hours = st.number_input("Hours per Laborer", min_value=0.0, value=8.0)
rate = st.number_input("Hourly Rate", min_value=0.0, value=55.0)

# Equipment
st.subheader("🚜 Equipment")
excavator = st.checkbox("Excavator ($400/day)")
skid_steer = st.checkbox("Skid Steer ($350/day)")
dump_truck = st.checkbox("Dump Truck ($300/day)")

# Travel
st.subheader("🚚 Travel")
trailer_km = st.number_input("Trailer Travel (km)", min_value=0.0, value=0.0)
passenger_km = st.number_input("Passenger Vehicle Travel (km)", min_value=0.0, value=0.0)

# Add-ons
st.subheader("➕ Add-ons")
include_fabric = st.checkbox("Include Geotextile Fabric ($0.50/sq ft)")
include_sand = st.checkbox("Include Polymeric Sand ($50/bag)")

# Calculate all costs
material_cost = calculate_material_cost(selected_material, sqft, data, margin)
gravel_cost, gravel_volume, gravel_loads = calculate_gravel_cost(sqft, depth)
fabric_cost = calculate_fabric_cost(sqft) if include_fabric else 0
bags, sand_cost = calculate_polymeric_sand(sqft, selected_material) if include_sand else (0, 0)
labor_cost = calculate_labor_cost(num_laborers, hours, rate)
equipment_cost = calculate_equipment_cost(excavator, skid_steer, dump_truck)
travel_cost = calculate_travel_cost(trailer_km, passenger_km)

# Totals
subtotal, hst, total = calculate_total(
    material_cost, gravel_cost, fabric_cost, sand_cost, labor_cost, equipment_cost, travel_cost
)

# Display results
st.subheader("💰 Quote Summary")
st.write(f"**Material Cost:** ${material_cost}")
st.write(f"**Gravel Cost:** ${gravel_cost} ({gravel_loads} loads, {gravel_volume} yd³)")
if include_fabric:
    st.write(f"**Fabric Cost:** ${fabric_cost}")
if include_sand:
    st.write(f"**Polymeric Sand:** ${sand_cost} ({bags} bags)")
st.write(f"**Labor Cost:** ${labor_cost}")
st.write(f"**Equipment Cost:** ${equipment_cost}")
st.write(f"**Travel Cost:** ${travel_cost}")
st.markdown("---")
st.write(f"**Subtotal:** ${subtotal}")
st.write(f"**HST (15%):** ${hst}")
st.write(f"### 💵 Grand Total: ${total}")
