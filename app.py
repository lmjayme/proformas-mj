import streamlit as st
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
import io

st.set_page_config(page_title="Generador de Proformas - MJ Logistics", layout="centered")

st.title("📋 Generador de Proformas Dinámicas")
st.write("Llena los datos para generar automáticamente tu PDF corporativo en una sola página.")

# 1. DATOS GENERALES
st.subheader("1. Datos Generales")
col1, col2 = st.columns(2)
with col1:
    nro_proforma = st.text_input("Número de Proforma", value="MJ260607")
    cliente = st.text_input("Cliente", value="ENERGY AND SOLUTIONS ELECTRICAL SAC")
with col2:
    fecha = st.date_input("Fecha")
    atencion = st.text_input("Atención", value="Srta. Encargada")

# 2. DATOS DE LA CARGA
st.subheader("2. Datos de la Carga")
col3, col4, col5 = st.columns(3)
with col3:
    tipo_servicio = st.text_input("Tipo de Servicio", value="LCL MARITIMO")
with col4:
    origen = st.text_input("Origen / Proveedor", value="Campinas - SP, Brazil")
with col5:
    peso_vol = st.text_input("Peso / Volumen", value="1 kl/vol")

# 3. COSTOS EN ORIGEN / FLETE
st.subheader("3. Costos en Origen / Flete (USD)")
col6, col7, col8 = st.columns(3)
with col6:
    flete = st.number_input("Flete", value=5.0)
with col7:
    gasto_local_origen = st.number_input("Gasto Local Origen", value=130.0)
with col8:
    total_exw = st.number_input("Total EXW", value=30.0)

# 4. COSTOS EN DESTINO (DINÁMICOS)
st.subheader("4. Costos en Destino / Gastos Locales")
st.write("Agrega o quita los conceptos que necesites para esta cotización:")

if 'gastos_destino' not in st.session_state:
    st.session_state.gastos_destino = [
        {"concepto": "DESCARGA", "monto": 35.40},
        {"concepto": "V°B°", "monto": 118.00},
        {"concepto": "TRANS. FEE.-", "monto": 35.40}
    ]

col_b1, col_b2 = st.columns(2)
with col_b1:
    if st.button("➕ Añadir Fila de Gasto"):
        st.session_state.gastos_destino.append({"concepto": "Nuevo Concepto", "monto": 0.0})
with col_b2:
    if st.button("❌ Eliminar Última Fila") and len(st.session_state.gastos_destino) > 0:
        st.session_state.gastos_destino.pop()

gastos_actualizados = []
for i, gasto in enumerate(st.session_state.gastos_destino):
    c1, c2 = st.columns([3, 1])
    with c1:
        nuevo_concepto = st.text_input(f"Concepto {i+1}", value=gasto["concepto"], key=f"concept_{i}")
    with c2:
        nuevo_monto = st.number_input(f"Monto {i+1} (USD)", value=gasto["monto"], key=f"monto_{i}", format="%.2f")
    gastos_actualizados.append({"concepto": nuevo_concepto, "monto": nuevo_monto})

st.session_state.gastos_destino = gastos_actualizados

# 5. IMPUESTOS Y PERCEPCIÓN
st.subheader("5. Impuestos de Aduana y Percepción (S/)")
col9, col10, col11 = st.columns(3)
with col9:
    fob = st.number_input("FOB", value=3442.0)
    flete_aprox = st.number_input("Flete Aprox", value=200.0)
with col10:
    seguro = st.number_input("Seguro", value=0.0)
    adv = st.number_input("ADV", value=0.0)
with col11:
    igv_imp = st.number_input("IGV de Importación", value=569.0)
    percepcion = st.number_input("Percepción", value=526.0)

total_flete_origen = flete + gasto_local_origen
total_origen = total_flete_origen + total_exw
total_gastos_locales = sum(gasto["monto"] for gasto in st.session_state.gastos_destino)

st.markdown("---")
if st.button("🚀 Generar y Descargar Proforma PDF"):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
    story = []
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle('TitleStyle', parent=styles['Heading1'], fontSize=16, textColor=colors.HexColor('#0F2C59'), spaceAfter=12)
    normal_style = styles['Normal']
    
    story.append(Paragraph(f"<b>PROFORMA: {nro_proforma}</b>", title_style))
    story.append(Paragraph(f"<b>Fecha:</b> {fecha} | <b>Cliente:</b> {cliente} | <b>Atención:</b> {atencion}", normal_style))
    story.append(Spacer(1, 15))
    
    data_carga = [
        ["Tipo de Servicio", "Origen / Proveedor", "Peso / Volumen"],
        [tipo_servicio, origen, peso_vol]
    ]
    t_carga = Table(data_carga, colWidths=[150, 250, 150])
    t_carga.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1E5128')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('BOTTOMPADDING', (0,0), (-1,0), 6),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold')
    ]))
    story.append(t_carga)
    story.append(Spacer(1, 15))
    
    data_costos = [
        ["CONCEPTO / DETALLE", "VALOR", "MONEDA"]
    ]
    data_costos.append(["[ORIGEN] Flete", f"{flete:.2f}", "USD"])
    data_costos.append(["[ORIGEN] Gasto Local Origen", f"{gasto_local_origen:.2f}", "USD"])
    data_costos.append(["[ORIGEN] Total EXW", f"{total_exw:.2f}", "USD"])
    data_costos.append(["TOTAL ORIGEN Y FLETE", f"{total_origen:.2f}", "USD"])
    
    data_costos.append(["<b>GASTOS EN DESTINO LOCALES</b>", "", ""])
    for g in st.session_state.gastos_destino:
        data_costos.append([g["concepto"], f"{g['monto']:.2f}", "USD"])
    data_costos.append(["TOTAL GASTOS LOCALES", f"{total_gastos_locales:.2f}", "USD"])
    
    data_costos.append(["<b>IMPUESTOS Y ADUANA</b>", "", ""])
    data_costos.append(["Valor FOB", f"{fob:.2f}", "S/"])
    data_costos.append(["IGV de Importación", f"{igv_imp:.2f}", "S/"])
    data_costos.append(["Percepción", f"{percepcion:.2f}", "S/"])
    
    t_costos = Table(data_costos, colWidths=[300, 150, 100])
    t_costos.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0F2C59')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('GRID', (0,0), (-1,-1), 0.5, colors.lightgrey),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('SPAN', (0,4), (2,4)),
        ('BACKGROUND', (0,4), (-1,4), colors.HexColor('#F8F9FA')),
        ('SPAN', (0,6+len(st.session_state.gastos_destino)), (2,6+len(st.session_state.gastos_destino))),
        ('BACKGROUND', (0,6+len(st.session_state.gastos_destino)), (-1,6+len(st.session_state.gastos_destino)), colors.HexColor('#F8F9FA')),
    ]))
    story.append(t_costos)
    
    doc.build(story)
    buffer.seek(0)
    
    st.download_button(
        label="📥 Hacer clic aquí para descargar PDF",
        data=buffer,
        file_name=f"PROFORMA_{nro_proforma}.pdf",
        mime="application/pdf"
    )
    st.success("¡PDF generado con éxito 
