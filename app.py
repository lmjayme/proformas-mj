import streamlit as st
import openpyxl
from openpyxl.drawing.image import Image
from datetime import date
import os
import io

st.set_page_config(page_title="MJ LOGISTIC - Editor Real", layout="wide")
st.title("💼 Generador de Proformas - MJ LOGISTIC")

# 1. CARGA DEL ARCHIVO
archivo_subido = st.file_uploader("📂 Selecciona tu archivo Excel (.xlsx):", type=["xlsx"])

if archivo_subido:
    # Leer el archivo desde la memoria
    bytes_data = archivo_subido.getvalue()
    wb = openpyxl.load_workbook(io.BytesIO(bytes_data))
    ws = wb.active
    
    st.success(f"✅ Archivo '{archivo_subido.name}' leído correctamente.")

    # 2. LECTURA Y EDICIÓN (Sin valores predeterminados "quemados")
    # Leemos lo que hay en la celda. Si está vacío, la caja estará vacía.
    with st.expander("📝 Datos Principales", expanded=True):
        col1, col2, col3 = st.columns(3)
        
        # Obtenemos los valores actuales del archivo
        nro = col1.text_input("Nro Proforma", value=str(ws['A4'].value or ""))
        cliente = col1.text_input("Cliente", value=str(ws['A9'].value or ""))
        
        # Fecha de hoy automática
        fecha = col2.text_input("Fecha", value=date.today().strftime("%Y-%m-%d"))
        
        atencion = col2.text_input("Atención", value=str(ws['C9'].value or "")) # Ajusta la celda si es otra
        servicio = col3.text_input("Servicio", value=str(ws['A12'].value or "")) # Ajusta la celda si es otra
        proveedor = col3.text_input("Proveedor", value=str(ws['A13'].value or "")) # Ajusta la celda si es otra

    # 3. GENERACIÓN FINAL
    if st.button("🚀 Guardar y Preparar Descarga"):
        # Logo
        if os.path.exists("logo.png"):
            img = Image("logo.png")
            img.width = 120 
            img.height = 40
            ws.add_image(img, 'A1')
            
        # Inyectar datos editados al Excel
        ws['A4'] = nro
        ws['A9'] = cliente
        ws['F5'] = fecha
        
        # Guardar en memoria
        output = io.BytesIO()
        wb.save(output)
        st.session_state.archivo_generado = output.getvalue()
        st.success("¡Datos inyectados! El archivo está listo.")

    # 4. DESCARGA
    if 'archivo_generado' in st.session_state:
        nombre_final = st.text_input("💾 Nombre para descargar:", f"PROFORMA_{nro}")
        st.download_button(
            label="📥 Descargar Excel",
            data=st.session_state.archivo_generado,
            file_name=f"{nombre_final}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
