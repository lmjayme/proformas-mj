import streamlit as st
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
import io

st.set_page_config(page_title="MJ LOGISTIC - Estructura Excel", layout="centered")

st.title("📋 Generador de Proformas - Formato Estructurado")
st.write("Introduce los datos. El sistema generará el PDF respetando el orden y la posición exacta de las celdas estilo Excel.")

# 1. CAPTURA DE DATOS DESDE EL CELULAR
st.subheader("Datos del Encabezado y Carga")
col1, col2 = st.columns(2)
with col1:
    nro_proforma = st.text_input("Número de Proforma", value="MJ240114")
    cliente = st.text_input("Señores (Cliente)", value="ENERGY AND SOLUTIONS ELECTRICAL SAC")
    atencion = st.text_input("Atención", value="Srta. Encargada")
with col2:
    fecha = st.date_input("Fecha de Emisión")
    tipo_servicio = st.text_input("Tipo de Servicio", value="LCL MARITIMO")
    peso_vol = st.text_input("Peso / Volumen", value="1 kl/vol")

st.subheader("Costos en Origen y Flete (USD)")
col3, col4, col5 = st.columns(3)
with col3:
    flete = st.number_input("FLETE", value=5.0)
with col4:
    local_charge = st.number_input("LOCAL CHARGE", value=130.0)
with col5:
    total_exw = st.number_input("TOTAL EXW", value=30.0)

st.subheader("Gastos Locales en Destino")
if 'gastos_destino' not in st.session_state:
    st.session_state.gastos_destino = [
        {"concepto": "DESCARGA", "monto": 35.40, "ref": "MIN. 30+IGV"},
        {"concepto": "V°B°", "monto": 118.00, "ref": "100+IGV"},
        {"concepto": "TRANS. FEE.-", "monto": 35.40, "ref": "30+IGV"}
    ]

col_b1, col_b2 = st.columns(2)
with col_b1:
    if st.button("➕ Añadir Gasto"):
        st.session_state.gastos_destino.append({"concepto": "Nuevo Gasto", "monto": 0.0, "ref": ""})
with col_b2:
    if st.button("❌ Quitar Gasto") and len(st.session_state.gastos_destino) > 0:
        st.session_state.gastos_destino.pop()

gastos_actualizados = []
for i, gasto in enumerate(st.session_state.gastos_destino):
    c1, c2, c3 = st.columns([2, 1, 1])
    with c1:
        nc = st.text_input(f"Concepto {i+1}", value=gasto["concepto"], key=f"c_{i}")
    with c2:
        nm = st.number_input(f"Monto {i+1}", value=gasto["monto"], key=f"m_{i}", format="%.2f")
    with c3:
        nr = st.text_input(f"Referencia {i+1}", value=gasto["ref"], key=f"r_{i}")
    gastos_actualizados.append({"concepto": nc, "monto": nm, "ref": nr})
st.session_state.gastos_destino = gastos_actualizados

st.subheader("Impuestos y Referenciales (S/)")
col6, col7, col8 = st.columns(3)
with col6:
    fob = st.number_input("FOB", value=3442.0)
with col7:
    flete_aprox = st.number_input("FLETE APROX", value=200.0)
with col8:
    igv_imp = st.number_input("IGV IMPORTACIÓN", value=569.0)
    percepcion = st.number_input("PERCEPCIÓN", value=526.0)

# CÁLCULOS AUTOMÁTICOS
total_flete = flete + local_charge
total_origen = total_flete + total_exw
total_gastos_locales = sum(g["monto"] for g in st.session_state.gastos_destino)
total_a_pagar = total_origen + total_gastos_locales

st.markdown("---")

if st.button("🚀 Generar PDF Estructurado Tipo Excel"):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=20, leftMargin=20, topMargin=20, bottomMargin=20)
    story = []
    
    styles = getSampleStyleSheet()
    style_title = ParagraphStyle('TStyle', fontName='Helvetica-Bold', fontSize=14, textColor=colors.HexColor('#0B2447'))
    style_normal = ParagraphStyle('Norm', fontName='Helvetica', fontSize=8.5, leading=11)
    style_bold = ParagraphStyle('Bld', fontName='Helvetica-Bold', fontSize=8.5, leading=11)
    style_right = ParagraphStyle('Rgt', fontName='Helvetica', fontSize=8.5, leading=11, alignment=2)
    style_right_bold = ParagraphStyle('RgtB', fontName='Helvetica-Bold', fontSize=8.5, leading=11, alignment=2)
    style_white_center = ParagraphStyle('WhtC', fontName='Helvetica-Bold', fontSize=8.5, textColor=colors.whitesmoke, alignment=1)

    # --- TÍTULO PRINCIPAL ---
    story.append(Paragraph(f"<b>MJ LOGISTIC & SYSTEMS E.I.R.L.</b>", style_title))
    story.append(Paragraph(f"<b>PROFORMA: {nro_proforma}</b>", ParagraphStyle('R', parent=style_bold, alignment=2)))
    story.append(Spacer(1, 10))
    
    # --- MATRIZ PRINCIPAL (Divide la pantalla en Bloque Izquierdo y Bloque Derecho en paralelo) ---
    # Columna 1: Datos del Cliente (Ancho 310) | Columna 2: Espacio (Ancho 20) | Columna 3: Costos Origen (Ancho 220)
    
    # Construcción de las filas internas de la sección de costos para poner a la derecha
    filas_matriz = [
        [Paragraph(f"<b>Señores:</b> {cliente}", style_normal), "", Paragraph("ORIGEN / FLETE TRÁMITE", style_white_center), Paragraph("VALOR", style_white_center)],
        [Paragraph(f"<b>Atención:</b> {atencion}", style_normal), "", Paragraph("FLETE", style_normal), Paragraph(f"{flete:.2f} USD", style_right)],
        [Paragraph(f"<b>Fecha:</b> {fecha}", style_normal), "", Paragraph("LOCAL CHARGE", style_normal), Paragraph(f"{local_charge:.2f} USD", style_right)],
        [Paragraph(f"<b>Servicio:</b> {tipo_servicio}", style_normal), "", Paragraph("<b>TOTAL FLETE</b>", style_bold), Paragraph(f"{total_flete:.2f} USD", style_right_bold)],
        [Paragraph(f"<b>Peso/Vol:</b> {peso_vol}", style_normal), "", Paragraph("TOTAL EXW", style_normal), Paragraph(f"{total_exw:.2f} USD", style_right)],
        ["", "", Paragraph("<b>TOTAL ORIGEN</b>", style_bold), Paragraph(f"{total_origen:.2f} USD", style_right_bold)]
    ]
    
    t_matriz = Table(filas_matriz, colWidths=[270, 15, 175, 90])
    t_matriz.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('SPAN', (0,0), (0,4)), # Une el bloque de datos del cliente para que se vea limpio a la izquierda
        ('BACKGROUND', (2,0), (3,0), colors.HexColor('#1F4E79')), # Encabezado Azul de Origen
        ('GRID', (2,0), (3,5), 0.5, colors.HexColor('#BDC3C7')), # Cuadrícula solo para la sección de costos
        ('BACKGROUND', (2,3), (3,3), colors.HexColor('#F2F4F4')),
        ('BACKGROUND', (2,5), (3,5), colors.HexColor('#EAEDED')),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_matriz)
    story.append(Spacer(1, 15))
    
    story.append(Paragraph("Por intermedio de la presente nos es grato saludarles y a la vez detallarles nuestra propuesta comercial de gastos locales:", style_normal))
    story.append(Spacer(1, 8))
    
    # --- TABLA DE GASTOS EN DESTINO (Alineada al mismo ancho total = 550) ---
    filas_destino = [
        [Paragraph("GASTO LOCAL EN DESTINO", style_white_center), Paragraph("MONTO", style_white_center), Paragraph("ESTADO / REF.", style_white_center)]
    ]
    for g in st.session_state.gastos_destino:
        filas_destino.append([Paragraph(g["concepto"], style_normal), Paragraph(f"{g['monto']:.2f} USD", style_right), Paragraph(g["ref"], style_normal)])
    filas_destino.append([Paragraph("<b>TOTAL GAST. LOCAL</b>", style_bold), Paragraph(f"{total_gastos_locales:.2f} USD", style_right_bold), Paragraph("INCL. IGV", style_bold)])
    
    t_dest = Table(filas_destino, colWidths=[270, 95, 185])
    t_dest.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1E8449')), # Encabezado Verde de Destino
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#BDC3C7')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BACKGROUND', (0,-1), (-1,-1), colors.HexColor('#E8F8F5')),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_dest)
    story.append(Spacer(1, 15))
    
    # --- TABLA DE IMPUESTOS Y RESUMEN FINAL ---
    filas_impuestos = [
        [Paragraph("IMPUESTOS + PERCEPCIÓN (REFERENCIAL ADUANA)", style_white_center), "", "", ""],
        [Paragraph(f"FOB: {fob:.2f} S/", style_normal), Paragraph(f"FLETE APROX: {flete_aprox:.2f} S/", style_normal), Paragraph(f"IGV IMP: {igv_imp:.2f} S/", style_normal), Paragraph(f"PERCEPCIÓN: {percepcion:.2f} S/", style_normal)],
        [Paragraph("<b>TOTAL ESTIMADO A PAGAR (ORIGEN + DESTINO)</b>", style_bold), "", "", Paragraph(f"<b>{total_a_pagar:.2f} USD</b>", style_right_bold)]
    ]
    t_imp = Table(filas_impuestos, colWidths=[200, 120, 110, 120])
    t_imp.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#7D6608')), # Encabezado Marrón de Aduana
        ('SPAN', (0,0), (3,0)),
        ('SPAN', (0,2), (2,2)), # Une el texto del total final
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#BDC3C7')),
        ('BACKGROUND', (0,-1), (-1,-1), colors.HexColor('#FDEDEC')), # Fondo rojo claro para resaltar el total
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_imp)
    
    # CONSTRUCCIÓN DEL ARCHIVO PDF
    doc.build(story)
    buffer.seek(0)
    
    st.download_button(
        label="📥 Descargar Proforma con Orden de Excel",
        data=buffer,
        file_name=f"PROFORMA_{nro_proforma}.pdf",
        mime="application/pdf"
    )
    st.success("¡Estructura fijada correctamente al formato de tu Excel!")
