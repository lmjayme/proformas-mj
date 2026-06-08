import streamlit as st
import openpyxl
from openpyxl.drawing.image import Image
from datetime import date
import os
import io # <--- IMPORTANTE: esto maneja el archivo en memoria

st.set_page_config(page_title="MJ LOGISTIC - Editor", layout="wide")
st.title("💼 Generador de Proformas - MJ LOGISTIC")

# 1. SUBIDA DEL ARCHIVO
archivo_subido = st.file_uploader("📂 Selecciona tu archivo Excel (.xlsx):", type=["xlsx"])

if archivo_subido:
    # --- AQUÍ ESTÁ EL CAMBIO ---
    # Leemos el archivo directamente desde la memoria (BytesIO)
    bytes_data = archivo_subido.getvalue()
    wb = openpyxl.load_workbook(io.BytesIO(bytes_data))
    ws = wb.active
    
    st.success(f"✅ Archivo '{archivo_subido.name}' cargado desde tu selección.")

    # 2. FORMULARIO DE EDICIÓN
    with st.expander("📝 Datos Principales", expanded=True):
        col1, col2, col3 = st.columns(3)
        nro = col1.text_input("Nro Proforma", "MJ240114")
        cliente = col1.text_input("Cliente", "ENERGY AND SOLUTIONS ELECTRICAL SAC")
        fecha = col2.text_input("Fecha", value=date.today().strftime("%Y-%m-%d"))
        atencion = col2.text_input("Atención", "Srta.")
        servicio = col3.text_input("Servicio", "LCL MARITIMO")
        proveedor = col3.text_input("Proveedor", "-")

    # ... (Tu lógica de gastos dinámicos aquí) ...
    # Asegúrate de mantener tu lógica de gastos igual.

    # 3. GENERACIÓN FINAL
    if st.button("🚀 Preparar Archivo para Descargar"):
        # Logo
        if os.path.exists("logo.png"):
            img = Image("logo.png")
            img.width = 120 
            img.height = 40
            ws.add_image(img, 'A1')
            
        # Inyectar
        ws['A4'] = f"PROFORMA {nro}"
        ws['A9'] = cliente
        ws['F5'] = fecha
        
        # Guardar en memoria para descarga (NO en disco)
        output = io.BytesIO()
        wb.save(output)
        st.session_state.archivo_generado = output.getvalue()
        st.success("¡Archivo listo! Ya puedes descargarlo.")

    # 4. DESCARGA
    if 'archivo_generado' in st.session_state:
        nombre_final = st.text_input("💾 Nombre del archivo (sin .xlsx):", f"PROFORMA_{nro}")
        st.download_button(
            label=f"📥 Descargar {nombre_final}.xlsx",
            data=st.session_state.archivo_generado,
            file_name=f"{nombre_final}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
