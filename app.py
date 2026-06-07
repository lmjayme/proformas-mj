import streamlit as st
import openpyxl
from openpyxl.utils import get_column_letter
import os

st.set_page_config(page_title="MJ LOGISTIC - Formato Real", layout="centered")

st.title("💼 Generador de Proformas - Formato Exacto Excel")
st.write("Escribe los datos aquí abajo y se estamparán directamente sobre tu plantilla original.")

# Verificar si el archivo Excel base existe en el repositorio
excel_plantilla = "PROFORMA MJ240114 ENERGY AND SOLUTIONS ELECTRICAL SAC (1).xlsx"

if not os.path.exists(excel_plantilla):
    st.error(f"⚠️ No se encuentra el archivo base '{excel_plantilla}' en tu GitHub. Por favor, súbelo para que funcione el formato.")
else:
    # 1. ENTRADA DE DATOS DESDE EL CELULAR
    st.subheader("Datos Generales")
    nro_proforma = st.text_input("Número de Proforma", value="MJ240114")
    cliente = st.text_input("Señores (Cliente)", value="ENERGY AND SOLUTIONS ELECTRICAL SAC")
    atencion = st.text_input("Atención", value="Srta. Encargada")
    
    st.subheader("Costos Principales (USD)")
    flete = st.number_input("FLETE", value=5.0)
    local_charge = st.number_input("LOCAL CHARGE", value=130.0)
    total_exw = st.number_input("TOTAL EXW", value=30.0)

    st.subheader("Impuestos y Aduana (S/)")
    fob = st.number_input("FOB", value=3442.0)
    flete_aprox = st.number_input("FLETE APROX", value=200.0)
    igv_imp = st.number_input("IGV IMPORTACIÓN", value=569.0)
    percepcion = st.number_input("PERCEPCIÓN", value=526.0)

    st.markdown("---")
    
    if st.button("🚀 Generar Proforma Idéntica al Excel"):
        # Abrir el Excel original manteniendo formatos y fórmulas
        wb = openpyxl.load_workbook(excel_plantilla, data_only=False)
        ws = wb.active
        
        # Mapeo de celdas exactas según tu estructura original
        ws['A4'] = f"PROFORMA {nro_proforma}"
        ws['A9'] = cliente
        ws['A10'] = f"Atención: {atencion}"
        
        # Valores numéricos en la columna de costos (Columna J / K según corresponda)
        ws['K5'] = flete
        ws['K9'] = local_charge
        ws['K11'] = total_exw
        
        # Datos de impuestos
        ws['B31'] = fob
        ws['B32'] = flete_aprox
        ws['E31'] = igv_imp
        ws['G31'] = percepcion
        
        # Guardar los cambios en un archivo temporal
        output_path = f"PROFORMA_{nro_proforma}.xlsx"
        wb.save(output_path)
        
        # Permitir la descarga directa del archivo con el formato clonado
        with open(output_path, "rb") as file:
            st.download_button(
                label="📥 Descargar archivo con Formato Original",
                data=file,
                file_name=f"PROFORMA_{nro_proforma}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        st.success("¡Tu proforma con formato exacto ha sido generada con éxito!")
