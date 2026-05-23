import streamlit as st
from fpdf import FPDF
import tempfile
from PIL import Image
import os

st.set_page_config(page_title="Field Research Report", layout="centered")

st.title("🧪 Field Research Reporting Tool")

# -----------------------------
# 1. USER INPUT
# -----------------------------
st.header("1. Research Information")

name = st.text_input("Researcher Name")
title = st.text_input("Discovery Title")
description = st.text_area("Description / Notes")

if not name:
    st.warning("⚠️ Please enter the Researcher Name")

if not title:
    st.warning("⚠️ Please enter a Discovery Title")

if not description:
    st.warning("⚠️ Please enter a Description")

# -----------------------------
# 2. GPS LOCATION
# -----------------------------
st.header("2. GPS Location")

lat = st.number_input("Latitude", format="%.6f")
lon = st.number_input("Longitude", format="%.6f")

valid_coords = True

if lat < -90 or lat > 90:
    st.warning("⚠️ Latitude must be between -90 and 90")
    valid_coords = False

if lon < -180 or lon > 180:
    st.warning("⚠️ Longitude must be between -180 and 180")
    valid_coords = False

if valid_coords:
    st.map({"lat": [lat], "lon": [lon]})

# -----------------------------
# 3. IMAGE UPLOAD
# -----------------------------
st.header("3. Visual Evidence")

image_file = st.file_uploader(
    "Upload Image",
    type=["jpg", "jpeg", "png", "webp", "bmp", "tiff"]
)

if image_file:
    st.image(image_file, caption="Uploaded Evidence", use_container_width=True)

# -----------------------------
# PDF GENERATION
# -----------------------------
def generate_pdf(name, title, description, lat, lon, image_file):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(0, 10, "Field Research Report", ln=True)

    pdf.ln(5)
    pdf.cell(0, 10, f"Researcher: {name}", ln=True)
    pdf.cell(0, 10, f"Title: {title}", ln=True)

    pdf.ln(5)
    pdf.multi_cell(0, 10, f"Description:\n{description}")

    pdf.ln(5)
    pdf.cell(0, 10, f"Latitude: {lat}", ln=True)
    pdf.cell(0, 10, f"Longitude: {lon}", ln=True)

    # -----------------------------
    # IMAGE HANDLING (FIXED)
    # -----------------------------
    if image_file:
        image = Image.open(image_file)

        # Convert everything to RGB PNG (FPDF safe)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
            image.convert("RGB").save(tmp.name, "PNG")
            tmp_path = tmp.name

        pdf.ln(5)
        pdf.image(tmp_path, w=100)

    pdf_path = "report.pdf"
    pdf.output(pdf_path)

    return pdf_path

# -----------------------------
# 4. GENERATE REPORT
# -----------------------------
st.header("4. Generate Report")

form_valid = (
    name and title and description and valid_coords and image_file is not None
)

if st.button("Generate PDF Report"):

    if not form_valid:
        st.error("❌ Please fix the warnings above before generating the report.")
    else:
        pdf_file = generate_pdf(name, title, description, lat, lon, image_file)

        with open(pdf_file, "rb") as f:
            st.download_button(
                label="📄 Download Report",
                data=f,
                file_name="field_report.pdf",
                mime="application/pdf"
            )

        st.success("✅ Report generated successfully!")