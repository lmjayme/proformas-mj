import streamlit as st
import openpyxl
from openpyxl.drawing.image import Image
from datetime import date
import os
import io

st.set_page_config(page_title="MJ LOGISTIC - Editor", layout="wide")
st.title("💼 Generador de Proformas - MJ LOGISTIC")

# 1. CARGA DEL ARCHIVO CON LIMPIEZA
archivo_subido = st.file_uploader("📂 Selecciona tu archivo Excel (.xlsx):", type=["xlsx"])

# Si subes un archivo nuevo, limpiamos la sesión anterior para que no haya mezclas
if archivo_subido:
    # Reiniciar el estado si cambiamos de archivo
    if 'nombre_archivo_anterior' not in st.session_state or st.session_state.nombre_archivo_anterior != archivo_subido.name:
        st.session_state.clear()
        st.session_state.nombre_archivo_anterior = archivo_subido.name
        st.rerun()

    # Procesar archivo
    bytes_data = archivo_subido.getvalue()
    wb = openpyxl.load_workbook(io.BytesIO(bytes_data))
    ws = wb.active
    st.success(f"✅ Archivo '{archivo_subido.name}' listo para editar.")

    # 2. DATOS PRINCIPALES
    with st.expander("📝 Datos Principales", expanded=True):
        col1, col2, col3 = st.columns(3)
        nro = col1.text_input("Nro Proforma", "MJ240114")
        cliente = col1.text_input("Cliente", "ENERGY AND SOLUTIONS ELECTRICAL SAC")
        fecha = col2.text_input("Fecha", value=date.today().strftime("%Y-%m-%d"))
        atencion = col2.text_input("Atención", "Srta.")
        servicio = col3.text_input("Servicio", "LCL MARITIMO")
        proveedor = col3.text_input("Proveedor", "-")

    # 3. GENERACIÓN FINAL
    if st.button("🚀 Procesar Cambios"):
        # Logo
        if os.path.exists("logo.png"):
            img = Image("logo.png")
            img.width = 120 
            img.height = 40
            ws.add_image(img, 'A1')
            
        # Inyectar (Asegúrate que estas celdas coincidan con tu Excel real)
        ws['A4'] = f"PROFORMA {nro}"
        ws['A9'] = cliente
        ws['F5'] = fecha
        
        output = io.BytesIO()
        wb.save(output)
        st.session_state.archivo_generado = output.getvalue()
        st.success("¡Archivo procesado! Ya puedes descargar.")

    # 4. DESCARGA
    if 'archivo_generado' in st.session_state:
        nombre_final = st.text_input("💾 Nombre para descargar:", f"PROFORMA_{nro}")
        st.download_button(
            label="📥 Descargar Excel",
            data=st.session_state.archivo_generado,
            file_name=f"{nombre_final}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
