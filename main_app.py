import streamlit as st
from utils import (
    load_paver_data, calculate_material_cost,
    calculate_gravel_cost, calculate_fabric_cost,
    calculate_polymeric_sand, calculate_labor_cost,
    calculate_equipment_cost, calculate_travel_cost,
    calculate_total
)

st.set_page_config("AKL Hardscape Master Tool", "🧱")
st.title("🧱 AKL Hardscape Master Tool")

st.sidebar.markdown("### 📂 Select Project Section")
section = st.sidebar.radio("", ["Walkway", "Retaining Wall", "Steps", "Fire Pit", "Quote Preview"])

if section == "Walkway":
    st.header("🚶‍♂️ Walkway Estimator")
    sqft = st.number_input("📐 Square Feet", min_value=0, step=1)
    margin_override = st.slider("📊 Override Margin %", 0, 100, 30)

    data = load_paver_data()
    data.columns = data.columns.str.strip()

    product = st.selectbox("🧱 Choose Product", data["Products"].dropna().unique())

    # Gravel
    st.subheader("🪨 Gravel")
    gravel_on = st.checkbox("Include Gravel Base", value=True)
    gravel_depth = st.number_input("Gravel Depth (inches)", value=6, step=1) if gravel_on else 0
    fabric_on = st.checkbox("Include Geotextile Fabric ($0.50/sq ft)", value=True)

    # Sand
    st.subheader("🧪 Polymeric Sand")
    sand_bags, sand_cost = calculate_polymeric_sand(sqft)

    # Labor
    st.subheader("👷 Labor")
    num_labor = st.number_input("Number of Laborers", 1, 10, 1)
    laborers = []
    for i in range(num_labor):
        col1, col2 = st.columns(2)
        with col1:
            rate = st.number_input(f"Laborer {i+1} Rate ($/hr)", value=35.0, step=5.0)
        with col2:
            hours = st.number_input(f"Laborer {i+1} Hours", value=8, step=1)
        laborers.append({"rate": rate, "hours": hours})

    # Equipment
    st.subheader("🚜 Equipment Use")
    excavator_hours = st.number_input("Excavator Hours", value=0, step=1)
    excavator_km = st.number_input("Excavator Trailer Km", value=0, step=1)
    skid_hours = st.number_input("Skid Steer Hours", value=0, step=1)
    skid_km = st.number_input("Skid Steer Trailer Km", value=0, step=1)
    dump_hours = st.number_input("Dump Truck Hours", value=0, step=1)
    dump_km = st.number_input("Dump Truck Trailer Km", value=0, step=1)

    # Passenger travel
    st.subheader("🚗 Passenger Travel")
    passenger_km = st.number_input("Round Trip Distance (km)", value=35, step=1)
    num_vehicles = st.number_input("Number of Passenger Vehicles", value=1, step=1)

    # Calculations
    material_cost = calculate_material_cost(product, sqft, data, margin_override)
    gravel_cost = calculate_gravel_cost(sqft, gravel_depth) if gravel_on else 0
    fabric_cost = calculate_fabric_cost(sqft) if fabric_on else 0
    labor_cost = calculate_labor_cost(laborers)
    equipment_cost = calculate_equipment_cost({
        "Excavator": excavator_hours,
        "Skid Steer": skid_hours,
        "Dump Truck": dump_hours
    })
    travel_cost = calculate_travel_cost(
        trailer_km=excavator_km + skid_km + dump_km,
        passenger_km=passenger_km,
        num_vehicles=num_vehicles
    )

    subtotal, tax, total = calculate_total(
        material_cost, gravel_cost, fabric_cost, sand_cost,
        labor_cost, equipment_cost, travel_cost
    )

    st.markdown("### 💵 Quote Summary")
    st.write(f"**Material Cost**: ${material_cost}")
    if gravel_on:
        st.write(f"**Gravel Cost**: ${gravel_cost}")
    if fabric_on:
        st.write(f"**Geotextile Fabric**: ${fabric_cost}")
    st.write(f"**Polymeric Sand**: ${sand_cost}")
    st.write(f"**Labor Cost**: ${labor_cost}")
    st.write(f"**Equipment Cost**: ${equipment_cost}")
    st.write(f"**Travel Cost**: ${travel_cost}")
    st.write(f"**Subtotal**: ${subtotal}")
    st.write(f"**HST (15%)**: ${tax}")
    st.success(f"**Grand Total: ${total}**")
