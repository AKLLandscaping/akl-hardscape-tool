import streamlit as st
import math
from utils import load_paver_data, calculate_material_cost

st.set_page_config(page_title="AKL Hardscape Master Tool", layout="wide")

st.markdown("## 🧱 AKL Hardscape Master Tool")
st.markdown("### 🧍‍♂️ Walkway Estimator")

# Load material data
paver_data = load_paver_data()

# Input: Square Footage
sqft = st.number_input("📏 Square Feet", min_value=0, value=0, step=1)

# Margin
margin = st.slider("📊 Override Margin %", 0, 100, 30)

# Product Selection
product = st.selectbox("🧱 Choose Product", paver_data["Products"].dropna().unique())

# Edge Restraint (auto)
edge_restraint_cost = 220  # per 100 sq ft
edge_units = math.ceil(sqft / 100)
edge_total = edge_units * edge_restraint_cost
edge_total_with_tax = round(edge_total * 1.15, 2)

# Inlay Option
inlay = st.checkbox("Add 4ft Inlay ($4000 + HST)?", value=False)
inlay_cost = 4000 * 1.15 if inlay else 0

# Gravel Add-on
gravel_addon_loads = st.selectbox("Extra Gravel Loads", options=list(range(0, 6)), index=0)
gravel_price_input = st.number_input("Extra Gravel Price per Load ($)", value=250, step=1)
gravel_delivery_km = st.number_input("Extra Gravel Delivery Km", value=30, step=1)
gravel_extra_km = max(0, gravel_delivery_km - 30)
gravel_delivery_cost = gravel_extra_km * 4.20
gravel_total_addon = round((gravel_addon_loads * gravel_price_input) + gravel_delivery_cost, 2)

# Polymeric Sand Option
sand_type = st.selectbox("Polymeric Sand Type", ["None", "Pavers", "Square Cut", "Random"])
if sand_type == "Pavers":
    sand_bag_coverage = 80
elif sand_type == "Square Cut":
    sand_bag_coverage = 120
elif sand_type == "Random":
    sand_bag_coverage = 50
else:
    sand_bag_coverage = 0

sand_bags = math.ceil(sqft / sand_bag_coverage) if sand_bag_coverage > 0 else 0
sand_total = round(sand_bags * 50 * 1.15, 2) if sand_bags else 0  # $50 per bag + tax

# Labor Section
st.markdown("### 🛠️ Labor")
num_laborers = st.selectbox("Number of Laborers", [1, 2, 3], index=1)
labor_inputs = []
for i in range(num_laborers):
    col1, col2 = st.columns(2)
    with col1:
        hours = st.selectbox(f"Hours for Laborer #{i+1}", options=list(range(1, 13)), index=7, key=f"hours_{i}")
    with col2:
        rate = st.selectbox(f"Hourly Rate for Laborer #{i+1}", [35, 40, 45, 50, 55, 60, 65], index=2, key=f"rate_{i}")
    labor_inputs.append((hours, rate))
labor_total = sum([h * r for h, r in labor_inputs])

# Equipment Section
st.markdown("### 🚜 Equipment Use")
excavator_hours = st.selectbox("Excavator Hours", list(range(0, 13)), index=1)
skid_steer_hours = st.selectbox("Skid Steer Hours", list(range(0, 13)), index=1)
dump_truck_hours = st.selectbox("Dump Truck Hours", list(range(0, 13)), index=1)
equipment_cost = (excavator_hours + skid_steer_hours + dump_truck_hours) * 130 * 1.15

# Trailer Transport
st.markdown("### 🚚 Travel")
excavator_km = st.number_input("Excavator Trailer Km", step=1, value=30)
skid_km = st.number_input("Skid Steer Trailer Km", step=1, value=30)
truck_km = st.number_input("Dump Truck Trailer Km", step=1, value=30)

def trailer_cost(km):
    return 250 if km <= 30 else 250 + (km - 30) * 4.20

trailer_total = sum([trailer_cost(km) for km in [excavator_km, skid_km, truck_km]]) * 1.15

# Passenger Vehicles
passenger_km = st.number_input("Passenger Vehicle Km", step=1, value=30)
vehicles = st.selectbox("Number of Passenger Vehicles", list(range(1, 6)), index=0)
passenger_travel_cost = round(passenger_km * 0.80 * vehicles, 2)

# Material Calculation
material = calculate_material_cost(product, sqft, paver_data, margin_override=margin)

# Gravel Base Calculation (auto)
gravel_cuft = sqft * 0.5  # 6" base = 0.5 ft
gravel_yards = math.ceil(gravel_cuft / 27)
gravel_base_cost = gravel_yards * 250  # $250/load

# Summary
st.markdown("## 📋 Estimate Summary")
st.write(f"**Product:** {product}")
st.write(f"**Price per Unit (with margin):** ${material['unit_price']}")
st.write(f"**Units Required:** {material['units_required']}")
st.write(f"**Material Total:** ${material['material_total']}")
st.markdown("---")
st.write(f"**Gravel Yards:** {gravel_yards} @ $250/yd = ${gravel_base_cost}")
st.write(f"**Edge Restraint:** {edge_units} x $220 = ${edge_total_with_tax}")
st.write(f"**Labor Total:** ${round(labor_total, 2)}")
st.write(f"**Equipment Cost:** ${round(equipment_cost, 2)}")
st.write(f"**Trailer Transport:** ${round(trailer_total, 2)}")
st.write(f"**Passenger Vehicle Travel:** ${passenger_travel_cost}")
st.write(f"**Extra Gravel Loads:** ${gravel_total_addon}")
if sand_total:
    st.write(f"**Polymeric Sand:** {sand_bags} bags = ${sand_total}")
if inlay_cost:
    st.write(f"**Inlay Option:** ${round(inlay_cost, 2)}")

# Totals
subtotal = (
    material["material_total"] + edge_total_with_tax + gravel_base_cost +
    labor_total + equipment_cost + trailer_total +
    passenger_travel_cost + gravel_total_addon + sand_total + inlay_cost
)
hst = round(subtotal * 0.15, 2)
grand_total = round(subtotal + hst, 2)

st.markdown("---")
st.markdown(f"**Subtotal:** ${round(subtotal, 2)}")
st.markdown(f"**HST (15%):** ${hst}")
st.markdown(f"### 💰 Final Total: ${grand_total}")
