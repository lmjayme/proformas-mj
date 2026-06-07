import streamlit as st
from fpdf import FPDF
import io

st.set_page_config(page_title="MJ LOGISTIC - PDF Profesional", layout="centered")

st.title("💼 Generador de Proformas - Formato Fiel")

# Datos del Cliente
cliente = st.text_input("Señores (Cliente)", "ENERGY AND SOLUTIONS ELECTRICAL SAC")
nro_proforma = st.text_input("Número de Proforma", "MJ240114")

if st.button("🚀 Generar PDF Fiel al Formato"):
    pdf = FPDF('P', 'mm', 'A4')
    pdf.add_page()
    
    # Encabezado
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "MJ LOGISTIC & SYSTEMS E.I.R.L.", 0, 1, 'L')
    pdf.set_font("Arial", '', 10)
    pdf.cell(0, 8, f"PROFORMA: {nro_proforma}", 0, 1, 'R')
    pdf.cell(0, 8, f"Señores: {cliente}", 0, 1, 'L')
    pdf.line(10, 35, 200, 35)
    
    # Tabla de Costos (Ejemplo de estructura rígida)
    pdf.ln(10)
    pdf.set_fill_color(31, 78, 121) # Azul corporativo
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(100, 8, "CONCEPTO", 1, 0, 'C', 1)
    pdf.cell(50, 8, "VALOR", 1, 1, 'C', 1)
    
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", '', 10)
    pdf.cell(100, 8, "FLETE", 1, 0, 'L')
    pdf.cell(50, 8, "5.00 USD", 1, 1, 'R')
    
    # Generar salida
    pdf_output = pdf.output(dest='S').encode('latin-1')
    
    st.download_button("📥 Descargar PDF Profesional", pdf_output, "proforma.pdf", "application/pdf")
    st.success("¡PDF generado sin errores de librería!")
