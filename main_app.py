
import streamlit as st
from utils import (
    render_header,
    load_shaw_products,
    calculate_walkway_cost,
    calculate_wall_cost,
    calculate_steps_cost,
    calculate_firepit_cost,
    render_quote_preview,
    generate_quote_pdf
)

st.set_page_config(page_title="AKL Hardscape Tool", layout="wide")
render_header()

section = st.sidebar.radio("📂 Select Project Section", [
    "Walkway", "Retaining Wall", "Steps", "Fire Pit", "📄 Quote Preview"
])

shaw_data = load_shaw_products()

if section == "Walkway":
    calculate_walkway_cost(shaw_data)
elif section == "Retaining Wall":
    calculate_wall_cost(shaw_data)
elif section == "Steps":
    calculate_steps_cost(shaw_data)
elif section == "Fire Pit":
    calculate_firepit_cost(shaw_data)
elif section == "📄 Quote Preview":
    render_quote_preview()
    pdf_bytes = generate_quote_pdf()
    st.download_button(
        label="📄 Download PDF Quote",
        data=pdf_bytes,
        file_name="AKL_Quote.pdf",
        mime="application/pdf"
    )
