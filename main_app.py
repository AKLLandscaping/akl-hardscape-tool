import streamlit as st
import pandas as pd
import math
from utils import load_paver_data, calculate_material_cost

# Constants
EDGE_RESTRAINT_COST = 220
INLAY_COST = 4000
GRAVEL_COST_PER_LOAD = 250
TRAILER_BASE_KM = 30
TRAILER_EXTRA_KM_RATE = 4.20
EQUIPMENT_RATE = 130
TAX_RATE = 0.15
PASSENGER_COST_PER_KM = 0.80
GEOTEXTILE_COST_PER_SQFT = 0.50

st.set_page_config(page_title="AKL Hardscape Master Tool", layout="wide")
st.title("🧱 AKL Hardscape Master Tool")
st.header("🧍‍♂️ Walkway Estimator")

# Load Material Data
data = load_paver_data()

# Inputs
sqft = st.number_input("📏 Square Feet", min_value=0, value=0, step=10)
margin = st.slider("📊 Override Margin %", 0, 100, 30)
product = st.selectbox("🎨 Choose Product", data["Products"].dropna().unique())

# ✅ Labor
st.subheader("👷 Labor")
num_laborers = st.selectbox("Number of Laborers", [1, 2, 3], index=1)
labor_total = 0
for i in range(num_laborers):
    hours = st.selectbox(f"Hours for Laborer #{i+1}", list(range(1, 13)), index=7, key=f"lab_hr_{i}")
    rate = st.selectbox(f"Hourly Pay for Laborer #{i+1}", [35, 40, 45, 50, 55, 60, 65], index=3, key=f"lab_rt_{i}")
    labor_total += hours * rate

# ✅ Equipment
st.subheader("🚜 Equipment Use")
excavator_hours = st.selectbox("Excavator Hours", list(range(0, 13)), index=1)
skid_hours = st.selectbox("Skid Steer Hours", list(range(0, 13)), index=1)
truck_hours = st.selectbox("Dump Truck Hours", list(range(0, 13)), index=1)

excavator_km = st.number_input("Excavator Trailer Km", value=30, step=1)
skid_km = st.number_input("Skid Steer Trailer Km", value=30, step=1)
truck_km = st.number_input("Dump Truck Trailer Km", value=30, step=1)

# ✅ Travel
st.subheader("🚗 Travel")
passenger_km = st.number_input("Round Trip Distance (km)", value=30, step=1)
passenger_vehicles = st.selectbox("Number of Passenger Vehicles", [1, 2, 3], index=0)

# ✅ Add-ons
st.subheader("➕ Add-Ons")

# Edge Restraint
edge_units = math.ceil(sqft / 100)
edge_total = edge_units * EDGE_RESTRAINT_COST
edge_total_tax = round(edge_total * (1 + TAX_RATE), 2)

# Inlay
inlay = st.checkbox("Include 4 ft wide inlay ($4000 + HST)", value=False)
inlay_total = round(INLAY_COST * (1 + TAX_RATE), 2) if inlay else 0

# Polymeric Sand
sand_type = st.selectbox("Polymeric Sand Type", ["None", "Pavers", "Square Cut", "Random"])
coverage_dict = {"Pavers": 80, "Square Cut": 120, "Random": 50}
sand_cost = 0
if sand_type != "None":
    bags = math.ceil(sqft / coverage_dict[sand_type])
    sand_cost = round(bags * 50 * (1 + TAX_RATE), 2)

# Gravel
gravel_depth_ft = 0.5
cubic_ft = sqft * gravel_depth_ft
gravel_yards = math.ceil(cubic_ft / 27)
gravel_base_cost = gravel_yards * GRAVEL_COST_PER_LOAD

# Extra Gravel Add-On
extra_loads = st.selectbox("Extra Gravel Loads", [0, 1, 2, 3], index=0)
gravel_price = st.number_input("Gravel Price per Load ($)", value=250, step=10)
gravel_km = st.number_input("Delivery Distance (km)", value=30, step=1)
extra_km = max(0, gravel_km - TRAILER_BASE_KM)
extra_gravel_cost = round(extra_loads * gravel_price + extra_km * TRAILER_EXTRA_KM_RATE, 2)

# Geotextile
st.subheader("🧵 Geotextile Fabric")
fabric_total = round(sqft * GEOTEXTILE_COST_PER_SQFT, 2)

# ✅ Calculate
try:
    mat = calculate_material_cost(product, sqft, data, margin)

    equipment_total = round((excavator_hours + skid_hours + truck_hours) * EQUIPMENT_RATE * (1 + TAX_RATE), 2)

    def trailer_cost(km): return 250 if km <= 30 else 250 + (km - 30) * TRAILER_EXTRA_KM_RATE
    trailer_total = sum([trailer_cost(x) for x in [excavator_km, skid_km, truck_km]])
    trailer_total = round(trailer_total * (1 + TAX_RATE), 2)

    passenger_cost = round(passenger_km * passenger_vehicles * PASSENGER_COST_PER_KM, 2)

    subtotal = sum([
        mat["material_total"],
        gravel_base_cost,
        extra_gravel_cost,
        fabric_total,
        edge_total_tax,
        labor_total,
        equipment_total,
        trailer_total,
        passenger_cost,
        sand_cost,
        inlay_total
    ])

    hst = round(subtotal * TAX_RATE, 2)
    final = round(subtotal + hst, 2)

    # ✅ Output
    st.markdown("## 📋 Estimate Summary")
    st.write(f"**Product:** {product}")
    st.write(f"**Price per Unit (with margin):** ${mat['unit_price']}")
    st.write(f"**Units Required:** {mat['units_required']}")
    st.write(f"**Material Total:** ${mat['material_total']}")

    st.write(f"**Gravel Yards:** {gravel_yards} @ $250/yd = ${gravel_base_cost}")
    st.write(f"**Extra Gravel Loads:** ${extra_gravel_cost}")
    st.write(f"**Geotextile Fabric Cost:** ${fabric_total}")
    st.write(f"**Edge Restraint:** {edge_units} x $220 = ${edge_total_tax}")
    st.write(f"**Labor Total:** ${labor_total}")
    st.write(f"**Equipment Cost:** ${equipment_total}")
    st.write(f"**Trailer Transport:** ${trailer_total}")
    st.write(f"**Passenger Vehicle Travel:** ${passenger_cost}")
    if sand_cost:
        st.write(f"**Polymeric Sand:** ${sand_cost}")
    if inlay_total:
        st.write(f"**Inlay Add-On:** ${inlay_total}")

    st.markdown("---")
    st.write(f"**Subtotal:** ${subtotal}")
    st.write(f"**HST (15%):** ${hst}")
    st.markdown(f"### 💰 Final Total: ${final}")

except Exception as e:
    st.error(f"Something went wrong: {e}")
