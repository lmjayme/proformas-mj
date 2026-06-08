import streamlit as st
import openpyxl
from openpyxl.drawing.image import Image
from datetime import date
import os
import uuid # Esto nos ayudará a crear un nombre único cada vez

st.set_page_config(page_title="MJ LOGISTIC - Editor Pro", layout="wide")
st.title("💼 Generador de Proformas - MJ LOGISTIC")

# 1. SUBIDA DEL ARCHIVO
archivo_subido = st.file_uploader("📂 Selecciona tu archivo Excel (.xlsx) desde tu celular:", type=["xlsx"])
archivo_logo = "logo.png"

if archivo_subido:
    # Creamos un nombre de archivo único para esta sesión para evitar confusiones
    nombre_unico = f"temp_{uuid.uuid4().hex}.xlsx"
    
    # Abrimos el archivo que subiste
    wb = openpyxl.load_workbook(archivo_subido)
    ws = wb.active
    
    # ... (Todo tu formulario de edición aquí) ...
    with st.expander("📝 Datos Principales", expanded=True):
        col1, col2, col3 = st.columns(3)
        nro = col1.text_input("Nro Proforma", "MJ240114")
        cliente = col1.text_input("Cliente", "ENERGY AND SOLUTIONS ELECTRICAL SAC")
        fecha_hoy = date.today().strftime("%Y-%m-%d")
        fecha = col2.text_input("Fecha", value=fecha_hoy)
        atencion = col2.text_input("Atención", "Srta.")
        servicio = col3.text_input("Servicio", "LCL MARITIMO")
        proveedor = col3.text_input("Proveedor", "-")

    # ... (Tu lógica de gastos y aduana igual) ...
    # (Asegúrate de mantener tu código de gastos dinámicos aquí)

    # 3. GENERACIÓN FINAL
    if st.button("🚀 Preparar Archivo para Guardar"):
        # ... (Tu lógica de insertar logo y datos) ...
        ws['A4'] = f"PROFORMA {nro}"
        ws['A9'] = cliente
        ws['F5'] = fecha
        
        # Guardamos usando el nombre único creado al principio
        wb.save(nombre_unico)
        st.session_state.archivo_generado = nombre_unico
        st.success("✅ Archivo procesado correctamente. ¡Listo para descargar!")

    # 4. DESCARGA
    if 'archivo_generado' in st.session_state:
        nombre_final = st.text_input("💾 Nombre del archivo (sin .xlsx):", f"PROFORMA_{nro}")
        with open(st.session_state.archivo_generado, "rb") as f:
            st.download_button(
                label=f"📥 Descargar {nombre_final}.xlsx",
                data=f,
                file_name=f"{nombre_final}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
