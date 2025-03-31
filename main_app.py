import streamlit as st
from utils import *

st.set_page_config(page_title="AKL Hardscape Master Tool", layout="wide")

st.title("🧱 AKL Hardscape Master Tool")

section = st.sidebar.radio("📂 Select Project Section", ["Walkway", "Retaining Wall", "Steps", "Fire Pit", "Quote Preview"])

if section == "Walkway":
    st.header("🚶‍♂️ Walkway Estimator")

    sqft = st.number_input("📏 Square Feet", min_value=0)
    margin = st.slider("🧮 Margin %", 0, 100, 30)

    data = load_paver_data()
    product_name = st.selectbox("🧱 Select Product", data["Products"].unique())

    laborers = []
    num_laborers = st.number_input("👷 Number of Laborers", min_value=1, value=1)
    for i in range(num_laborers):
        rate = st.number_input(f"Laborer {i+1} Hourly Rate ($)", value=55.0)
        hours = st.number_input(f"Laborer {i+1} Hours Worked", value=8.0)
        laborers.append({"rate": rate, "hours": hours})

    st.subheader("🚜 Equipment")
    excavator_hours = st.number_input("Excavator Hours", value=0)
    skid_steer_hours = st.number_input("Skid Steer Hours", value=0)
    dump_truck_hours = st.number_input("Dump Truck Hours", value=0)

    equipment = [
        {"name": "Excavator", "hours": excavator_hours},
        {"name": "Skid Steer", "hours": skid_steer_hours},
        {"name": "Dump Truck", "hours": dump_truck_hours}
    ]

    st.subheader("🚗 Travel")
    trailer_km = st.number_input("Trailer Transport Distance (km)", value=0)
    passenger_km = st.number_input("Passenger Vehicle Distance (km)", value=0)
    num_vehicles = st.number_input("Number of Passenger Vehicles", value=1, min_value=1)

    if sqft and product_name:
        mat_total, pallets = calculate_material_cost(product_name, sqft, data, margin)
        labor_total = calculate_labor_cost(laborers)
        equip_total = calculate_equipment_cost(equipment)
        travel_total = calculate_travel_cost(trailer_km, passenger_km, num_vehicles)

        subtotal, hst, grand = calculate_total(mat_total, labor_total, equip_total, travel_total)

        st.success(f"💰 Material Total: ${mat_total}")
        st.success(f"👷 Labor Total: ${labor_total}")
        st.success(f"🚜 Equipment Total: ${equip_total}")
        st.success(f"🚗 Travel Total: ${travel_total}")
        st.info(f"🧾 Subtotal: ${subtotal} | HST: ${hst} | Grand Total: ${grand}")
    else:
        st.info("Please enter square footage and select a product to begin.")
