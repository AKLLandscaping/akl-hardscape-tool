
import streamlit as st
import pandas as pd
from io import BytesIO
from xhtml2pdf import pisa

# Equipment pricing based on AKL price list
EQUIPMENT_RATES = {
    "Excavator": 130,
    "Skid Steer": 100,
    "Dump Truck": 120
}

def render_header():
    st.markdown("""
        <div style='background-color:#1e1e1e; padding:1rem; display:flex; justify-content:space-between; align-items:center;'>
            <div><img src='https://i.imgur.com/kgrxAsP.png' height='50'></div>
            <div style='color:white; text-align:right;'>
                <p style='margin:0;'>📞 <b>902-802-4563</b><br>
                🌐 <a href='http://www.AKLLandscaping.com' style='color:#a3e635;'>www.AKLLandscaping.com</a></p>
            </div>
        </div>
    """, unsafe_allow_html=True)

def load_shaw_products():
    return pd.read_excel("shaw_products.xlsx")

def global_cost_inputs():
    st.markdown("### 🛠️ Equipment, Labor & Travel")
    num_laborers = st.number_input("Number of Laborers", min_value=0, value=2)
    hours_per_laborer = st.number_input("Total Hours per Laborer", min_value=0.0, value=8.0)
    labor_rate = st.select_slider("Labor Rate per Hour", options=[35, 40, 45, 50, 55, 60, 65], value=65)

    st.markdown("#### 🚜 Equipment Hours")
    equipment_hours = {}
    for eq in EQUIPMENT_RATES:
        equipment_hours[eq] = st.number_input(f"{eq} Hours", min_value=0.0, value=0.0)

    st.markdown("#### 🚚 Travel")
    trailer_km = st.number_input("Trailer Transport Distance (km)", min_value=0.0, value=0.0)
    passenger_km = st.number_input("Passenger Vehicle Distance (km)", min_value=0.0, value=0.0)

    # Calculations
    labor_cost = num_laborers * hours_per_laborer * labor_rate
    equipment_cost = sum(equipment_hours[eq] * EQUIPMENT_RATES[eq] for eq in EQUIPMENT_RATES)
    trailer_trips = (trailer_km / 25)
    trailer_cost = trailer_trips * 250
    passenger_cost = passenger_km * 0.80
    travel_total = trailer_cost + passenger_cost

    return labor_cost, equipment_cost, travel_total

def calculate_total_with_addons(material_cost, labor, equipment, travel):
    subtotal = material_cost + labor + equipment + travel
    hst = subtotal * 0.15
    total = subtotal + hst
    return subtotal, hst, total

def calculate_walkway_cost(data):
    st.subheader("🚶‍♂️ Walkway Calculator")
    sqft = st.number_input("Square Feet", min_value=0)
    product = st.selectbox("Material", data['Product Name'].unique())
    try:
        unit_price = float(data.loc[data['Product Name'] == product, 'Contractor Price'].values[0])
    except:
        st.error("❌ Price not found for this product.")
        return
    material_cost = unit_price * sqft
    labor_cost, equipment_cost, travel_cost = global_cost_inputs()
    subtotal, hst, total = calculate_total_with_addons(material_cost, labor_cost, equipment_cost, travel_cost)
    st.markdown(f"**Total: ${total:,.2f} (incl. HST)**")

def calculate_wall_cost(data):
    st.subheader("🧱 Retaining Wall Calculator")
    length = st.number_input("Wall Length (ft)", min_value=0.0)
    height = st.number_input("Wall Height (ft)", min_value=0.0)
    wall_area = length * height
    product = st.selectbox("Wall Block Type", data['Product Name'].unique())
    try:
        unit_price = float(data.loc[data['Product Name'] == product, 'Contractor Price'].values[0])
    except:
        st.error("❌ Price not found for this wall block.")
        return
    base_depth = st.number_input("Base Gravel Depth (inches)", value=12)
    gravel_volume = wall_area * 1.25 * (base_depth / 12)
    gravel_cost = gravel_volume / 3 * 250
    geotextile = st.checkbox("Include Geotextile Fabric ($0.50/sqft)?")
    fabric_cost = wall_area * 0.5 if geotextile else 0
    material_cost = unit_price * wall_area + gravel_cost + fabric_cost
    labor_cost, equipment_cost, travel_cost = global_cost_inputs()
    subtotal, hst, total = calculate_total_with_addons(material_cost, labor_cost, equipment_cost, travel_cost)
    st.markdown(f"**Total: ${total:,.2f} (incl. HST)**")

def calculate_steps_cost(data):
    st.subheader("🪜 Steps Calculator")
    num_steps = st.number_input("Number of Steps", min_value=0)
    product = st.selectbox("Step Material", data['Product Name'].unique())
    try:
        unit_price = float(data.loc[data['Product Name'] == product, 'Contractor Price'].values[0])
    except:
        st.error("❌ No price found for this material. Check 'Contractor Price' in Excel.")
        return
    gravel_base = st.checkbox("Install on Gravel Base?")
    gravel_cost = num_steps * 25 if gravel_base else 0
    adhesive = st.checkbox("Include Adhesive ($15/tube per 20 ft)?")
    adhesive_cost = 15 * (num_steps // 2) if adhesive else 0
    material_cost = (num_steps * unit_price) + gravel_cost + adhesive_cost
    labor_cost, equipment_cost, travel_cost = global_cost_inputs()
    subtotal, hst, total = calculate_total_with_addons(material_cost, labor_cost, equipment_cost, travel_cost)
    st.markdown(f"**Total: ${total:,.2f} (incl. HST)**")

def calculate_firepit_cost(data):
    st.subheader("🔥 Fire Pit Calculator")
    num_pits = st.number_input("Number of Fire Pits", min_value=0)
    product = st.selectbox("Fire Pit Kit", data['Product Name'].unique())
    try:
        unit_price = float(data.loc[data['Product Name'] == product, 'Contractor Price'].values[0])
    except:
        st.error("❌ Price not found for this fire pit material.")
        return
    adhesive = st.checkbox("Include Adhesive ($15)?")
    base_gravel = st.checkbox("Install on Gravel Base ($75)?")
    base_cost = 75 if base_gravel else 0
    adhesive_cost = 15 if adhesive else 0
    material_cost = (num_pits * unit_price) + base_cost + adhesive_cost
    labor_cost, equipment_cost, travel_cost = global_cost_inputs()
    subtotal, hst, total = calculate_total_with_addons(material_cost, labor_cost, equipment_cost, travel_cost)
    st.markdown(f"**Total: ${total:,.2f} (incl. HST)**")

def render_quote_preview():
    st.subheader("📄 Quote Preview")
    st.write("Client Name: [Client]")
    st.write("Job Site Address: [Address]")
    st.write("Phone/Email: [Phone] / [Email]")
    st.write("Summary of quote will appear here...")

def generate_quote_pdf():
    html = "<h1>AKL Quote</h1><p>This is the quote PDF content</p>"
    pdf = BytesIO()
    pisa.CreatePDF(html, dest=pdf)
    return pdf.getvalue()
