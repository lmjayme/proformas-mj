import streamlit as st
import openpyxl
import os

st.set_page_config(page_title="MJ LOGISTIC - Proforma Total", layout="wide")
st.title("💼 Generador Proformas - MJ LOGISTIC")

plantilla = "PROFORMA MJ240114 ENERGY AND SOLUTIONS ELECTRICAL SAC (1).xlsx"

if not os.path.exists(plantilla):
    st.error("⚠️ Sube el archivo Excel al repositorio.")
else:
    # --- FORMULARIO DE DATOS ---
    with st.expander("📝 Datos Principales", expanded=True):
        c1, c2, c3 = st.columns(3)
        nro = c1.text_input("Nro Proforma", "MJ240114")
        cliente = c1.text_input("Cliente", "ENERGY AND SOLUTIONS ELECTRICAL SAC")
        fecha = c2.text_input("Fecha", "2026-06-07")
        atencion = c2.text_input("Atención", "Srta.")
        servicio = c3.text_input("Servicio", "LCL MARITIMO")
        proveedor = c3.text_input("Proveedor", "-")

    # --- GASTOS DINÁMICOS (Aquí metes Comisión, Adm, etc.) ---
    st.subheader("➕ Gastos Operativos y Destino")
    if 'gastos' not in st.session_state:
        st.session_state.gastos = [
            {"concepto": "DESCARGA", "monto": 35.4, "ref": "MIN. 30+IGV"},
            {"concepto": "V°B°", "monto": 118.0, "ref": "100+IGV"},
            {"concepto": "COMISIÓN", "monto": 0.0, "ref": ""},
            {"concepto": "GASTOS ADM.", "monto": 0.0, "ref": ""}
        ]

    for i, g in enumerate(st.session_state.gastos):
        cols = st.columns([3, 1, 1, 1])
        st.session_state.gastos[i]['concepto'] = cols[0].text_input(f"Concepto {i+1}", g['concepto'], key=f"c{i}")
        st.session_state.gastos[i]['monto'] = cols[1].number_input(f"Monto {i+1}", value=float(g['monto']), key=f"m{i}")
        st.session_state.gastos[i]['ref'] = cols[2].text_input(f"Ref {i+1}", g['ref'], key=f"r{i}")
        if cols[3].button("🗑️", key=f"d{i}"):
            st.session_state.gastos.pop(i)
            st.rerun()

    if st.button("➕ Agregar Concepto Extra"):
        st.session_state.gastos.append({"concepto": "", "monto": 0.0, "ref": ""})
        st.rerun()

    # --- GENERACIÓN ---
    if st.button("🚀 Generar Excel Completo"):
        wb = openpyxl.load_workbook(plantilla)
        ws = wb.active
        
        # Inyectar datos fijos
        ws['A4'] = f"PROFORMA {nro}"
        ws['A9'] = cliente
        ws['F5'] = fecha
        
        # Escribir gastos dinámicos empezando en fila 20 (ajusta si es necesario)
        fila = 20
        for g in st.session_state.gastos:
            ws.cell(row=fila, column=9, value=g['concepto']) # Columna I
            ws.cell(row=fila, column=10, value=g['monto'])    # Columna J
            ws.cell(row=fila, column=12, value=g['ref'])      # Columna L
            fila += 1
            
        archivo = f"PROFORMA_{nro}.xlsx"
        wb.save(archivo)
        with open(archivo, "rb") as f:
            st.download_button("📥 Descargar Proforma Final", f, archivo)
        st.success("¡Excel generado con todos los campos!")
