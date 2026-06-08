import streamlit as st
import openpyxl
import io
from datetime import date

st.set_page_config(page_title="MJ LOGISTIC - Editor Real", layout="wide")
st.title("💼 Generador de Proformas - MJ LOGISTIC")

archivo_subido = st.file_uploader("📂 Selecciona tu archivo Excel (.xlsx):", type=["xlsx"])

if archivo_subido:
    # 1. CARGA SEGURA
    bytes_data = archivo_subido.getvalue()
    wb = openpyxl.load_workbook(io.BytesIO(bytes_data), data_only=False)
    ws = wb.active
    
    # 2. CARGA DE DATOS AL ESTADO (Solo al subir el archivo)
    if 'gastos' not in st.session_state:
        st.session_state.gastos = []
        for fila in range(20, 50): # Escaneamos filas 20 a 50
            concepto = ws.cell(row=fila, column=9).value
            monto = ws.cell(row=fila, column=10).value
            ref = ws.cell(row=fila, column=12).value
            
            if concepto is not None: # Si hay algo escrito
                st.session_state.gastos.append({
                    "concepto": str(concepto),
                    "monto": float(monto) if monto else 0.0,
                    "ref": str(ref) if ref else ""
                })

    # 3. INTERFAZ (Formulario)
    with st.expander("📝 Datos Principales", expanded=True):
        c1, c2 = st.columns(2)
        nro = c1.text_input("Nro Proforma", value=str(ws['A4'].value or ""))
        cliente = c2.text_input("Cliente", value=str(ws['A9'].value or ""))

    st.subheader("➕ Gastos y Conceptos")
    for i, g in enumerate(st.session_state.gastos):
        cols = st.columns([3, 1, 2, 1])
        st.session_state.gastos[i]['concepto'] = cols[0].text_input(f"C{i}", g['concepto'], key=f"c{i}")
        st.session_state.gastos[i]['monto'] = cols[1].number_input(f"M{i}", value=float(g['monto']), key=f"m{i}")
        st.session_state.gastos[i]['ref'] = cols[2].text_input(f"R{i}", g['ref'], key=f"r{i}")
        if cols[3].button("🗑️", key=f"del_{i}"):
            st.session_state.gastos.pop(i)
            st.rerun()

    if st.button("➕ Agregar Fila"):
        st.session_state.gastos.append({"concepto": "", "monto": 0.0, "ref": ""})
        st.rerun()

    # 4. GUARDADO FORZADO
    if st.button("🚀 GRABAR EN EXCEL"):
        # Limpiar área
        for fila in range(20, 51):
            ws.cell(row=fila, column=9, value=None)
            ws.cell(row=fila, column=10, value=None)
            ws.cell(row=fila, column=12, value=None)
            
        # Escribir nuevos
        for i, g in enumerate(st.session_state.gastos):
            ws.cell(row=20+i, column=9, value=g['concepto'])
            ws.cell(row=20+i, column=10, value=g['monto'])
            ws.cell(row=20+i, column=12, value=g['ref'])
            
        ws['A4'] = nro
        ws['A9'] = cliente
        
        # Guardar en buffer fresco
        output = io.BytesIO()
        wb.save(output)
        st.session_state.archivo_generado = output.getvalue()
        st.success("✅ ¡Datos grabados! Descarga tu archivo.")

    if 'archivo_generado' in st.session_state:
        st.download_button("📥 Descargar Excel", st.session_state.archivo_generado, "Proforma_Final.xlsx")
