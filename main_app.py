import streamlit as st
from utils import (
    load_paver_data,
    load_wall_data,
    load_steps_data,
    load_firepit_data,
    load_garden_wall_data,
    load_extras_data,
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

section = st.sidebar.radio("📂 Select Project Section", ["Walkway", "Retaining Wall", "Steps", "Fire Pit"])

# Shared margin input
margin_percent = st.sidebar.slider("📈 Margin %", 0, 100, 30)

# Shared inputs
sqft = st.number_input("🔲 Square Footage (or # Units for EA)", min_value=0.0, value=100.0)
depth = st.number_input("📏 Gravel Base Depth (inches)", min_value=0.0, value=6.0)

# Labor
st.markdown("### 👷 Labor")
labor_entries = []
num_laborers = st.number_input("Number of Laborers", min_value=0, value=1)
for i in range(num_laborers):
    col1, col2 = st.columns(2)
    with col1:
        rate = st.number_input(f"Laborer {i+1} Rate ($/hr)", min_value=0.0, value=50.0)
    with col2:
        hours = st.number_input(f"Laborer {i+1} Hours", min_value=0.0, value=8.0)
    labor_entries.append({"rate": rate, "hours": hours})

# Equipment
st.markdown("### 🚜 Equipment")
excavator = st.checkbox("Excavator ($400)")
skid_steer = st.checkbox("Skid Steer ($350)")
dump_truck = st.checkbox("Dump Truck ($300)")

# Travel
st.markdown("### 🚚 Travel")
trailer_km = st.number_input("Trailer Travel (km)", min_value=0.0, value=0.0)
passenger_km = st.number_input("Passenger Vehicle Travel (km)", min_value=0.0, value=0.0)

# Load the correct data for the section
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

# Filter only the expected columns
columns_to_show = ["Product Name", "Pallet Qty", "Unit", "Contractor", "Net", "Margin", "TOTAL"]
filtered_data = data[columns_to_show]

# Material selector
st.markdown("### 🧱 Select Material")
material_options = filtered_data["Product Name"].unique()
selected_material = st.selectbox("Choose a material", material_options)

# Cost Calculations
material_cost = calculate_material_cost(selected_material, sqft, data, margin_percent)
gravel_cost, gravel_volume, gravel_loads = calculate_gravel_cost(sqft, depth)
fabric_cost = calculate_fabric_cost(sqft)
bags, sand_cost = calculate_polymeric_sand(sqft, selected_material)
labor_cost = calculate_labor_cost(labor_entries)
equipment_cost = calculate_equipment_cost(excavator, skid_steer, dump_truck)
travel_cost = calculate_travel_cost(trailer_km, passenger_km)

# Totals
subtotal, hst, grand_total = calculate_total(
    material_cost, gravel_cost, fabric_cost, sand_cost, labor_cost, equipment_cost, travel_cost
)

# Display
st.markdown("## 💵 Quote Summary")
st.write(f"**Material Cost:** ${material_cost}")
st.write(f"**Gravel Cost:** ${gravel_cost} ({gravel_loads} loads, {gravel_volume} yd³)")
st.write(f"**Fabric Cost:** ${fabric_cost}")
st.write(f"**Polymeric Sand:** ${sand_cost} ({bags} bags)")
st.write(f"**Labor Cost:** ${labor_cost}")
st.write(f"**Equipment Cost:** ${equipment_cost}")
st.write(f"**Travel Cost:** ${travel_cost}")

st.markdown("### 💰 Total")
st.write(f"**Subtotal:** ${subtotal}")
st.write(f"**HST (15%):** ${hst}")
st.write(f"**Grand Total:** ${grand_total}")
