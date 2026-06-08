import streamlit as st
import openpyxl
from datetime import date
import io

st.set_page_config(page_title="MJ LOGISTIC - Editor Pro", layout="wide")
st.title("💼 Generador de Proformas - MJ LOGISTIC")

# 1. CARGA DEL ARCHIVO
archivo_subido = st.file_uploader("📂 Selecciona tu archivo Excel (.xlsx):", type=["xlsx"])

if archivo_subido:
    bytes_data = archivo_subido.getvalue()
    wb = openpyxl.load_workbook(io.BytesIO(bytes_data))
    ws = wb.active
    
    # --- INICIALIZAR ESTADO SI ES NUEVO ARCHIVO ---
    if 'gastos' not in st.session_state or st.session_state.get('archivo_actual') != archivo_subido.name:
        st.session_state.archivo_actual = archivo_subido.name
        # Extraemos los gastos reales desde el Excel (ejemplo: filas 20 a 40)
        lista_temporal = []
        for fila in range(20, 40):
            concepto = ws.cell(row=fila, column=9).value
            monto = ws.cell(row=fila, column=10).value
            ref = ws.cell(row=fila, column=12).value
            if concepto:
                lista_temporal.append({"concepto": concepto, "monto": float(monto or 0), "ref": str(ref or "")})
        st.session_state.gastos = lista_temporal

    # 2. FORMULARIO (Como antes)
    with st.expander("📝 Datos Principales", expanded=True):
        col1, col2 = st.columns(2)
        nro = col1.text_input("Nro Proforma", value=str(ws['A4'].value or "MJ240114"))
        cliente = col1.text_input("Cliente", value=str(ws['A9'].value or ""))
        fecha = col2.text_input("Fecha", value=date.today().strftime("%Y-%m-%d"))

    # 3. GASTOS DINÁMICOS (Interfaz de cajitas)
    st.subheader("➕ Gastos y Conceptos")
    for i, g in enumerate(st.session_state.gastos):
        cols = st.columns([3, 1, 2, 1])
        st.session_state.gastos[i]['concepto'] = cols[0].text_input(f"Concepto {i+1}", g['concepto'], key=f"c{i}")
        st.session_state.gastos[i]['monto'] = cols[1].number_input(f"Monto {i+1}", value=float(g['monto']), key=f"m{i}")
        st.session_state.gastos[i]['ref'] = cols[2].text_input(f"Ref {i+1}", g['ref'], key=f"r{i}")
        if cols[3].button("🗑️", key=f"d{i}"):
            st.session_state.gastos.pop(i)
            st.rerun()

    if st.button("➕ Agregar Fila"):
        st.session_state.gastos.append({"concepto": "", "monto": 0.0, "ref": ""})
        st.rerun()

    # 4. GENERACIÓN FINAL
    if st.button("🚀 Guardar Cambios"):
        ws['A4'] = nro
        ws['A9'] = cliente
        ws['F5'] = fecha
        
        # Guardar gastos
        for i, g in enumerate(st.session_state.gastos):
            ws.cell(row=20+i, column=9, value=g['concepto'])
            ws.cell(row=20+i, column=10, value=g['monto'])
            ws.cell(row=20+i, column=12, value=g['ref'])
            
        output = io.BytesIO()
        wb.save(output)
        st.session_state.archivo_generado = output.getvalue()
        st.success("¡Archivo listo para descargar!")

    if 'archivo_generado' in st.session_state:
        st.download_button("📥 Descargar Excel", st.session_state.archivo_generado, "Proforma_Editada.xlsx")
