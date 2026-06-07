import streamlit as st
import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
import io

st.set_page_config(page_title="MJ LOGISTIC & SYSTEMS - Proformas", layout="centered")

st.title("💼 Sistema de Proformas - MJ LOGISTIC & SYSTEMS")
st.write("Genera tus cotizaciones con el formato exacto del Excel original.")

# 1. ENCABEZADO Y DATOS GENERALES
st.subheader("1. Datos Principales de la Proforma")
col1, col2 = st.columns(2)
with col1:
    nro_proforma = st.text_input("Número de Proforma", value="MJ240114")
    cliente = st.text_input("Señores (Cliente)", value="ENERGY AND SOLUTIONS ELECTRICAL SAC")
    atencion = st.text_input("Atención", value="Srta. Encargada")
with col2:
    fecha = st.date_input("Fecha de Emisión")
    proveedor = st.text_input("Proveedor", value="-")

# 2. DATOS DE LA CARGA Y FLETE
st.subheader("2. Detalles de la Carga")
col3, col4, col5 = st.columns(3)
with col3:
    tipo_servicio = st.text_input("Tipo de Servicio", value="LCL MARITIMO")
    peso_vol = st.text_input("Peso / Volumen", value="1 kl/vol")
with col4:
    contenido = st.text_input("Contenido de Carga", value="CARGA GENERAL, NO IMO")
    origen = st.text_input("Origen (Dirección)", value="Rua Alfredo da Costa Figo, n°. 102 | Campinas - SP, Brazil")
with col5:
    flete_val = st.number_input("Flete (USD)", value=5.0)
    gasto_local_origen = st.number_input("Local Charge Origen (USD)", value=130.0)
    total_exw = st.number_input("Total EXW (USD)", value=30.0)

# 3. GASTOS LOCALES EN DESTINO (DINÁMICOS)
st.subheader("3. Gastos en Destino (Aumentar o quitar celdas)")
st.write("Modifica los conceptos. Al final se sumarán automáticamente y se calculará el IGV.")

if 'gastos_destino' not in st.session_state:
    st.session_state.gastos_destino = [
        {"concepto": "DESCARGA", "monto": 35.40, "detalle": "MIN. 30+IGV"},
        {"concepto": "V°B°", "monto": 118.00, "detalle": "100+IGV"},
        {"concepto": "TRANS. FEE.-", "monto": 35.40, "detalle": "30+IGV"}
    ]

col_b1, col_b2 = st.columns(2)
with col_b1:
    if st.button("➕ Aumentar Celda / Costo"):
        st.session_state.gastos_destino.append({"concepto": "Nuevo Concepto", "monto": 0.0, "detalle": ""})
with col_b2:
    if st.button("❌ Quitar Última Celda") and len(st.session_state.gastos_destino) > 0:
        st.session_state.gastos_destino.pop()

gastos_actualizados = []
for i, gasto in enumerate(st.session_state.gastos_destino):
    c1, c2, c3 = st.columns([2, 1, 1])
    with c1:
        nc = st.text_input(f"Concepto {i+1}", value=gasto["concepto"], key=f"c_{i}")
    with c2:
        nm = st.number_input(f"Monto {i+1} (S/ o USD)", value=gasto["monto"], key=f"m_{i}", format="%.2f")
    with c3:
        nd = st.text_input(f"Referencia {i+1}", value=gasto["detalle"], key=f"d_{i}")
    gastos_actualizados.append({"concepto": nc, "monto": nm, "detalle": nd})

st.session_state.gastos_destino = gastos_actualizados

# 4. IMPUESTOS + PERCEPCIÓN
st.subheader("4. Impuestos + Percepción (S/)")
col6, col7, col8 = st.columns(3)
with col6:
    fob = st.number_input("FOB", value=3442.0)
    flete_aprox = st.number_input("Flete Aprox", value=200.0)
with col7:
    seguro = st.number_input("Seguro", value=30.0)
    adv = st.number_input("ADV", value=0.0)
with col8:
    igv_imp = st.number_input("IGV de Importación", value=569.0)
    percepcion = st.number_input("Percepción", value=526.0)

# BOTÓN DE GENERACIÓN
st.markdown("---")
if st.button("🚀 Generar PDF con Formato de Excel Original"):
    buffer = io.BytesIO()
    # Configuración de hoja A4 con márgenes optimizados para 1 sola página
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=25, leftMargin=25, topMargin=25, bottomMargin=25)
    story = []
    
    styles = getSampleStyleSheet()
    header_style = ParagraphStyle('HStyle', fontName='Helvetica-Bold', fontSize=14, textColor=colors.HexColor('#0B2447'))
    txt_normal = ParagraphStyle('TNormal', fontName='Helvetica', fontSize=9, leading=11)
    txt_bold = ParagraphStyle('TBold', fontName='Helvetica-Bold', fontSize=9, leading=11)
    txt_white_bold = ParagraphStyle('TWBold', fontName='Helvetica-Bold', fontSize=9, textColor=colors.whitesmoke, alignment=1)
    
    # --- ENCABEZADO CORPORATIVO ---
    encabezado_data = [
        [Paragraph(f"<b>PROFORMA {nro_proforma}</b>", header_style), "", Paragraph(f"<b>FECHA:</b> {fecha}", txt_normal)],
        [Paragraph(f"<b>Señores:</b> {cliente}", txt_normal), "", Paragraph(f"<b>PROVEEDOR:</b> {proveedor}", txt_normal)],
        [Paragraph(f"<b>Atención:</b> {atencion}", txt_normal), "", Paragraph(f"<b>PESO/VOL:</b> {peso_vol}", txt_normal)],
        [Paragraph(f"<i>{tipo_servicio} - {contenido}</i>", txt_normal), "", ""]
    ]
    t_encabezado = Table(encabezado_data, colWidths=[280, 40, 220])
    t_encabezado.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
    ]))
    story.append(t_encabezado)
    story.append(Spacer(1, 10))
    
    story.append(Paragraph("Por intermedio de la presente nos es grato saludarles y a la vez detallarles nuestra propuesta comercial:", txt_normal))
    story.append(Spacer(1, 10))
    
    # --- TABLA DE COSTOS DE ORIGEN Y FLETE ---
    total_flete = flete_val + gasto_local_origen
    total_origen = total_flete + total_exw
    
    tabla_origen_data = [
        [Paragraph("ORIGEN / FLETE TRÁMITE", txt_white_bold), Paragraph("VALOR", txt_white_bold), Paragraph("MONEDA", txt_white_bold)],
        [Paragraph("FLETE", txt_normal), f"{flete_val:.2f}", "USD"],
        [Paragraph("LOCAL CHARGE", txt_normal), f"{gasto_local_origen:.2f}", "USD"],
        [Paragraph("<b>TOTAL FLETE</b>", txt_bold), f"<b>{total_flete:.2f}</b>", "USD"],
        [Paragraph("TOTAL EXW", txt_normal), f"{total_exw:.2f}", "USD"],
        [Paragraph("<b>TOTAL ORIGEN</b>", txt_bold), f"<b>{total_origen:.2f}</b>", "USD"]
    ]
    t_origen = Table(tabla_origen_data, colWidths=[340, 100, 100])
    t_origen.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#2C3E50')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.lightgrey),
        ('ALIGN', (1,1), (1,-1), 'RIGHT'),
        ('ALIGN', (2,1), (2,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BACKGROUND', (0,3), (-1,3), colors.HexColor('#EAEDED')),
        ('BACKGROUND', (0,5), (-1,5), colors.HexColor('#D6DBDF')),
    ]))
    story.append(t_origen)
    story.append(Spacer(1, 12))
    
    # --- TABLA DE GASTOS LOCALES EN DESTINO ---
    tabla_destino_data = [
        [Paragraph("GASTO LOCAL EN DESTINO", txt_white_bold), Paragraph("MONTO", txt_white_bold), Paragraph("ESTADO / REF.", txt_white_bold)]
    ]
    
    total_gasto_local = 0.0
    for g in st.session_state.gastos_destino:
        tabla_destino_data.append([Paragraph(g["concepto"], txt_normal), f"{g['monto']:.2f}", Paragraph(g["detalle"], txt_normal)])
        total_gasto_local += g["monto"]
        
    tabla_destino_data.append([Paragraph("<b>TOTAL GAST. LOCAL</b>", txt_bold), f"<b>{total_gasto_local:.2f}</b>", "INCL. IGV"])
    
    t_destino = Table(tabla_destino_data, colWidths=[340, 100, 100])
    t_destino.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1E8449')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.lightgrey),
        ('ALIGN', (1,1), (1,-1), 'RIGHT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BACKGROUND', (0,-1), (-1,-1), colors.HexColor('#D5F5E3')),
    ]))
    story.append(t_destino)
    story.append(Spacer(1, 12))
    
    # --- TABLA DE IMPUESTOS Y ADUANA ---
    valor_cif = fob + flete_aprox + seguro
    total_impuestos = adv + igv_imp + 92.0 # Incorporando IPM referencial del Excel original
    
    tabla_imp_data = [
        [Paragraph("IMPUESTOS + PERCEPCIÓN (REFERENCIAL ADUANA)", txt_white_bold), "", ""],
        [Paragraph("FOB:", txt_normal), f"{fob:.2f}", "S/"],
        [Paragraph("FLETE APROX:", txt_normal), f"{flete_aprox:.2f}", "S/"],
        [Paragraph("SEGURO:", txt_normal), f"{seguro:.2f}", "S/"],
        [Paragraph("<b>VALOR CIF:</b>", txt_bold), f"<b>{valor_cif:.2f}</b>", "S/"],
        [Paragraph("IGV DE IMPORTACIÓN:", txt_normal), f"{igv_imp:.2f}", "S/"],
        [Paragraph("PERCEPCIÓN APODERADA:", txt_normal), f"{percepcion:.2f}", "S/"],
        [Paragraph("<b>TOTAL A PAGAR ESTIMADO</b>", txt_bold), f"<b>{(total_gasto_local + total_origen):.2f}</b>", "USD"]
    ]
    t_imp = Table(tabla_imp_data, colWidths=[340, 100, 100])
    t_imp.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#7D6608')),
        ('SPAN', (0,0), (2,0)),
        ('GRID', (0,0), (-1,-1), 0.5, colors.lightgrey),
        ('ALIGN', (1,1), (1,-1), 'RIGHT'),
        ('BACKGROUND', (0,4), (-1,4), colors.HexColor('#FCF3CF')),
        ('BACKGROUND', (0,-1), (-1,-1), colors.HexColor('#FADBD8')),
    ]))
    story.append(t_imp)
    
    # CONSTRUCCIÓN DEL DOCUMENTO
    doc.build(story)
    buffer.seek(0)
    
    st.download_button(
        label="📥 Descargar Proforma Oficial PDF",
        data=buffer,
        file_name=f"PROFORMA_{nro_proforma}.pdf",
        mime="application/pdf"
    )
    st.success("¡Proforma estructurada correctamente al formato original!")
