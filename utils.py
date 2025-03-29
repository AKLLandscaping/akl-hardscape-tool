
import streamlit as st
import pandas as pd
from io import BytesIO
from xhtml2pdf import pisa

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

def calculate_walkway_cost(data):
    st.subheader("🚶‍♂️ Walkway Calculator")
    sqft = st.number_input("Square Feet", min_value=0)
    product = st.selectbox("Material", data['Product Name'].unique())
    unit_price = data.loc[data['Product Name'] == product, 'Contractor Price'].values[0]
    labor_rate = st.number_input("Labor Rate per Hour", value=65.0)
    labor_hours = st.number_input("Estimated Labor Hours", value=8.0)
    material_total = unit_price * sqft
    labor_total = labor_rate * labor_hours
    hst = 0.15 * (material_total + labor_total)
    total = material_total + labor_total + hst
    st.markdown(f"**Total: ${total:,.2f} (incl. HST)**")

def calculate_wall_cost(data):
    st.subheader("🧱 Retaining Wall Calculator")
    length = st.number_input("Wall Length (ft)", min_value=0.0)
    height = st.number_input("Wall Height (ft)", min_value=0.0)
    wall_area = length * height
    product = st.selectbox("Wall Block Type", data['Product Name'].unique())
    unit_price = data.loc[data['Product Name'] == product, 'Contractor Price'].values[0]
    base_depth = st.number_input("Base Gravel Depth (inches)", value=12)
    gravel_volume = wall_area * 1.25 * (base_depth / 12)
    gravel_cost = gravel_volume / 3 * 250
    geotextile = st.checkbox("Include Geotextile Fabric ($0.50/sqft)?")
    fabric_cost = wall_area * 0.5 if geotextile else 0
    material_total = unit_price * wall_area
    hst = 0.15 * (material_total + gravel_cost + fabric_cost)
    total = material_total + gravel_cost + fabric_cost + hst
    st.markdown(f"**Total: ${total:,.2f} (incl. HST)**")

def calculate_steps_cost(data):
    st.subheader("🪜 Steps Calculator")
    num_steps = st.number_input("Number of Steps", min_value=0)
    product = st.selectbox("Step Material", data['Product Name'].unique())
    unit_price = data.loc[data['Product Name'] == product, 'Contractor Price'].values[0]
    gravel_base = st.checkbox("Install on Gravel Base?")
    gravel_cost = num_steps * 25 if gravel_base else 0
    adhesive = st.checkbox("Include Adhesive ($15/tube per 20 ft)?")
    adhesive_cost = 15 * (num_steps // 2) if adhesive else 0
    step_total = num_steps * unit_price
    hst = 0.15 * (step_total + gravel_cost + adhesive_cost)
    total = step_total + gravel_cost + adhesive_cost + hst
    st.markdown(f"**Total: ${total:,.2f} (incl. HST)**")

def calculate_firepit_cost(data):
    st.subheader("🔥 Fire Pit Calculator")
    num_pits = st.number_input("Number of Fire Pits", min_value=0)
    product = st.selectbox("Fire Pit Kit", data['Product Name'].unique())
    unit_price = data.loc[data['Product Name'] == product, 'Contractor Price'].values[0]
    adhesive = st.checkbox("Include Adhesive ($15)?")
    base_gravel = st.checkbox("Install on Gravel Base ($75)?")
    base_cost = 75 if base_gravel else 0
    adhesive_cost = 15 if adhesive else 0
    pit_total = num_pits * unit_price
    hst = 0.15 * (pit_total + base_cost + adhesive_cost)
    total = pit_total + base_cost + adhesive_cost + hst
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
