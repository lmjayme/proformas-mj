import streamlit as st
import openpyxl
from openpyxl.drawing.image import Image
import os

st.set_page_config(page_title="MJ LOGISTIC - Proforma Final", layout="wide")
st.title("💼 Generador de Proformas - MJ LOGISTIC")

# Configuración de archivos
plantilla = "PROFORMA MJ240114 ENERGY AND SOLUTIONS ELECTRICAL SAC (1).xlsx"
archivo_logo = "logo.png"

if not os.path.exists(plantilla):
    st.error(f"⚠️ No encuentro el archivo: {plantilla}")
else:
    # 1. ENTRADA DE DATOS
    with st.expander("📝 Datos del Cliente y Carga", expanded=True):
        c1, c2, c3 = st.columns(3)
        nro = c1.text_input("Nro Proforma", "MJ240114")
        cliente = c1.text_input("Cliente", "ENERGY AND SOLUTIONS ELECTRICAL SAC")
        fecha = c2.text_input("Fecha", "2026-06-07")
        atencion = c2.text_input("Atención", "Srta.")
        servicio = c3.text_input("Servicio", "LCL MARITIMO")
        proveedor = c3.text_input("Proveedor", "-")

    # 2. GASTOS DINÁMICOS
    st.subheader("➕ Gastos y Conceptos")
    if 'gastos' not in st.session_state:
        st.session_state.gastos = [{"concepto": "DESCARGA", "monto": 35.4, "ref": "INCL. IGV"}, {"concepto": "V°B°", "monto": 118.0, "ref": "INCL. IGV"}]

    for i, g in enumerate(st.session_state.gastos):
        cols = st.columns([3, 1, 1, 1])
        st.session_state.gastos[i]['concepto'] = cols[0].text_input(f"Concepto {i+1}", g['concepto'], key=f"c{i}")
        st.session_state.gastos[i]['monto'] = cols[1].number_input(f"Monto {i+1}", value=float(g['monto']), key=f"m{i}")
        st.session_state.gastos[i]['ref'] = cols[2].text_input(f"Ref {i+1}", g['ref'], key=f"r{i}")
        if cols[3].button("🗑️", key=f"d{i}"):
            st.session_state.gastos.pop(i)
            st.rerun()

    if st.button("➕ Agregar Fila"):
        st.session_state.gastos.append({"concepto": "", "monto": 0.0, "ref": ""})
        st.rerun()

    # 3. GENERACIÓN FINAL
    if st.button("🚀 Generar Excel Final"):
        wb = openpyxl.load_workbook(plantilla)
        ws = wb.active
        
        # Insertar Logo
        if os.path.exists(archivo_logo):
            img = Image(archivo_logo)
            img.width = 120 # Ajusta el tamaño a tu gusto
            img.height = 40
            ws.add_image(img, 'A1') 
            
        # Inyectar datos fijos
        ws['A4'] = f"PROFORMA {nro}"
        ws['A9'] = cliente
        ws['F5'] = fecha
        
        # Inyectar gastos en tabla (empezando fila 20)
        fila = 20
        for g in st.session_state.gastos:
            ws.cell(row=fila, column=9, value=g['concepto'])
            ws.cell(row=fila, column=10, value=g['monto'])
            ws.cell(row=fila, column=12, value=g['ref'])
            fila += 1
            
        archivo_final = f"PROFORMA_{nro}.xlsx"
        wb.save(archivo_final)
        
        with open(archivo_final, "rb") as f:
            st.download_button("📥 Descargar Proforma Completa", f, archivo_final)
        st.success("¡Archivo listo con logo y datos!")
