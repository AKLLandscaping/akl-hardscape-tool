import streamlit as st
from utils import (
    load_paver_data,
    calculate_material_cost,
    calculate_gravel_cost,
    calculate_fabric_cost,
    calculate_polymeric_sand,
    calculate_labor_cost,
    calculate_equipment_cost,
    calculate_trailer_cost,
    calculate_passenger_vehicle_cost,
    calculate_total
)

st.set_page_config(page_title="AKL Hardscape Master Tool", layout="centered")
st.title("🧱 AKL Hardscape Master Tool")

section = st.radio("📂 Select Project Section", ["Walkway"])

if section == "Walkway":
    st.header("🚶 Walkway Estimator")
    sqft = st.number_input("Square Feet", min_value=0)

    data = load_paver_data()
    margin_override = st.slider("📊 Override Margin %", 0, 100, 30) / 100

    product_list = data["Products"].dropna().unique()
    product = st.selectbox("🧱 Choose Product", product_list)

    include_lifter = st.checkbox("Include Lifter Rental ($100)", value=False)

    st.markdown("### 🪨 Gravel")
    include_gravel = st.checkbox("Include Gravel Base", value=True)
    gravel_depth = st.number_input("Gravel Depth (inches)", value=6)
    gravel_cost = fabric_cost = 0
    if include_gravel:
        gravel_cost, _, _ = calculate_gravel_cost(sqft, gravel_depth)
        include_fabric = st.checkbox("Include Geotextile Fabric ($0.50/sq ft)", value=True)
        fabric_cost = calculate_fabric_cost(sqft) if include_fabric else 0

    st.markdown("### 🧪 Polymeric Sand")
    bags, sand_cost = calculate_polymeric_sand(sqft, product)
    st.write(f"Bags needed: {bags} | Sand Cost: ${sand_cost:.2f}")

    st.markdown("### 👷 Labor")
    laborers = []
    num_laborers = st.number_input("Number of Laborers", 1, 5, value=2)
    for i in range(num_laborers):
        col1, col2 = st.columns(2)
        with col1:
            rate = st.number_input(f"Laborer {i+1} Rate ($/hr)", min_value=0, value=50)
        with col2:
            hours = st.number_input(f"Laborer {i+1} Hours", min_value=0.0, value=8.0)
        laborers.append({'rate': rate, 'hours': hours})
    labor_cost = calculate_labor_cost(laborers)

    st.markdown("### 🚜 Equipment Use")
    excavator_hrs = st.number_input("Excavator Hours", value=0.0)
    excavator_km = st.number_input("Excavator Trailer Km", value=0)
    skid_steer_hrs = st.number_input("Skid Steer Hours", value=0.0)
    skid_steer_km = st.number_input("Skid Steer Trailer Km", value=0)
    dump_truck_hrs = st.number_input("Dump Truck Hours", value=0.0)
    dump_truck_km = st.number_input("Dump Truck Trailer Km", value=0)

    equipment_cost = calculate_equipment_cost(excavator_hrs, skid_steer_hrs, dump_truck_hrs)
    trailer_cost = sum([
        calculate_trailer_cost(excavator_km) if excavator_hrs else 0,
        calculate_trailer_cost(skid_steer_km) if skid_steer_hrs else 0,
        calculate_trailer_cost(dump_truck_km) if dump_truck_hrs else 0,
    ])

    st.markdown("### 🚗 Passenger Travel")
    passenger_km = st.number_input("Round Trip Distance (km)", value=0)
    vehicles = st.number_input("Number of Passenger Vehicles", min_value=1, max_value=5, value=1)
    passenger_cost = calculate_passenger_vehicle_cost(passenger_km, vehicles)

    st.markdown("## 🧾 Total")
    material_cost = calculate_material_cost(product, sqft, data, margin_override=margin_override)
    lifter_cost = 100 if include_lifter else 0

    subtotal, hst, grand_total = calculate_total(
        material_cost, gravel_cost, fabric_cost, sand_cost,
        lifter_cost, labor_cost, equipment_cost, trailer_cost, passenger_cost
    )

    st.write(f"**Material Cost:** ${material_cost:.2f}")
    st.write(f"**Gravel:** ${gravel_cost:.2f} | Fabric: ${fabric_cost:.2f}")
    st.write(f"**Sand:** ${sand_cost:.2f} | Lifter: ${lifter_cost:.2f}")
    st.write(f"**Labor:** ${labor_cost:.2f} | Equipment: ${equipment_cost:.2f}")
    st.write(f"**Trailer:** ${trailer_cost:.2f} | Passenger: ${passenger_cost:.2f}")
    st.markdown(f"**Subtotal:** ${subtotal:.2f}")
    st.markdown(f"**HST (15%):** ${hst:.2f}")
    st.markdown(f"### ✅ Grand Total: ${grand_total:.2f}")
