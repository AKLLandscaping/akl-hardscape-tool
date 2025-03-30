import streamlit as st
from utils import *
import math

st.set_page_config(page_title="AKL Hardscape Master Tool", layout="wide")
st.title("🧱 AKL Hardscape Master Tool")

# Sidebar navigation
section = st.sidebar.radio("📁 Select Project Section", ["Walkway", "Retaining Wall", "Steps", "Fire Pit", "Quote Preview"])

if section == "Walkway":
    st.header("🚶 Walkway Estimator")

    sqft = st.number_input("📐 Square Feet", min_value=0, step=10)

    margin_override = st.slider("📊 Override Margin %", 0, 100, 30)

    paver_data = load_paver_data()
    product_options = paver_data["Products"].dropna().unique()
    product_choice = st.selectbox("🧱 Choose Product", product_options)

    # Optional gravel base
    use_gravel = st.checkbox("🪨 Include Gravel Base", value=True)
    gravel_depth = st.number_input("Gravel Depth (inches)", value=6) if use_gravel else 0

    # Geotextile fabric
    use_fabric = st.checkbox("📏 Include Geotextile Fabric ($0.50/sq ft)", value=True)

    # Polymeric Sand
    st.subheader("🧪 Polymeric Sand")
    material_type = product_choice
    sand_bags, sand_cost = calculate_polymeric_sand(sqft, material_type)
    st.markdown(f"**Sand Needed:** {sand_bags} bags — ${sand_cost:.2f}")

    # Labor
    st.subheader("👷 Labor")
    num_laborers = st.slider("Number of Laborers", 1, 4, 2)
    labor_inputs = []
    for i in range(num_laborers):
        with st.expander(f"Laborer {i+1}"):
            hours = st.number_input(f"Hours Worked (Laborer {i+1})", value=8, step=1)
            rate = st.number_input(f"Hourly Rate (Laborer {i+1})", value=35, step=1)
            labor_inputs.append((hours, rate))

    total_labor = sum([h * r for h, r in labor_inputs])

    # Equipment
    st.subheader("🚜 Equipment Use")
    eq_inputs = {}
    for eq in ["Excavator", "Skid Steer", "Dump Truck"]:
        with st.expander(eq):
            hours = st.number_input(f"{eq}_
