import streamlit as st
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
import io

st.set_page_config(page_title="MJ LOGISTIC & SYSTEMS - PDF Directo", layout="centered")

st.title("📋 Generador de Proformas PDF Oficiales")
st.write("Introduce los datos. El sistema generará un PDF estructurado en una sola hoja A4.")

# 1. ENTRADA DE DATOS DESDE EL CELULAR
st.subheader("1. Datos de la Proforma")
col1, col2 = st.columns(2)
with col1:
    nro_proforma = st.text_input("Número de Proforma", value="MJ240114")
    cliente = st.text_input("Señores (Cliente)", value="ENERGY AND SOLUTIONS ELECTRICAL SAC")
    atencion = st.text_input("Atención", value="Srta. Encargada")
with col2:
    fecha = st.date_input("Fecha de Emisión")
    tipo_servicio = st.text_input("Tipo de Servicio", value="LCL MARITIMO")
    peso_vol = st.text_input("Peso / Volumen", value="1 kl/vol")

st.subheader("2. Costos en Origen / Flete (USD)")
col3, col4, col5 = st.columns(3)
with col3:
    flete = st.number_input("FLETE", value=5.0)
with col4:
    local_charge = st.number_input("LOCAL CHARGE", value=130.0)
with col5:
    total_exw = st.number_input("TOTAL EXW", value=30.0)

st.subheader("3. Gastos Locales en Destino (Ajustable)")
# Estructura de gastos dinámicos idéntica a tu plantilla
if 'gastos_destino' not in st.session_state:
    st.session_state.gastos_destino = [
        {"concepto": "DESCARGA", "monto": 35.40, "ref": "MIN. 30+IGV"},
        {"concepto": "V°B°", "monto": 118.00, "ref": "100+IGV"},
        {"concepto": "TRANS. FEE.-", "monto": 35.40, "ref": "30+IGV"}
    ]

col_b1, col_b2 = st.columns(2)
with col_b1:
    if st.button("➕ Añadir Fila de Costo"):
        st.session_state.gastos_destino.append({"concepto": "Nuevo Concepto", "monto": 0.0, "ref": ""})
with col_b2:
    if st.button("❌ Quitar Última Fila") and len(st.session_state.gastos_destino) > 0:
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

st.subheader("4. Impuestos y Referenciales (S/)")
col6, col7, col8 = st.columns(3)
with col6:
    fob = st.number_input("FOB", value=3442.0)
with col7:
    flete_aprox = st.number_input("FLETE APROX", value=200.0)
with col8:
    igv_imp = st.number_input("IGV IMPORTACIÓN", value=569.0)
    percepcion = st.number_input("PERCEPCIÓN", value=526.0)

# CÁLCULOS MATEMÁTICOS AUTOMÁTICOS
total_flete_origen = flete + local_charge
total_origen = total_flete_origen + total_exw
total_gastos_locales = sum(g["monto"] for g in st.session_state.gastos_destino)

st.markdown("---")

if st.button("🚀 Generar y Descargar PDF Oficial"):
    buffer = io.BytesIO()
    # Ajuste estricto de márgenes (20mm) para forzar que todo quepa en una sola hoja A4
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=20, leftMargin=20, topMargin=20, bottomMargin=20)
    story = []
    
    styles = getSampleStyleSheet()
    
    # Definición de tipografías y tamaños compactos para evitar saltos de página
    style_company = ParagraphStyle('CompStyle', fontName='Helvetica-Bold', fontSize=14, textColor=colors.HexColor('#0B2447'))
    style_proforma = ParagraphStyle('ProfStyle', fontName='Helvetica-Bold', fontSize=12, textColor=colors.HexColor('#2C3E50'), alignment=2)
    style_normal = ParagraphStyle('Norm', fontName='Helvetica', fontSize=8.5, leading=11)
    style_bold = ParagraphStyle('Bld', fontName='Helvetica-Bold', fontSize=8.5, leading=11)
    style_white = ParagraphStyle('Wht', fontName='Helvetica-Bold', fontSize=8.5, textColor=colors.whitesmoke, alignment=1)
    
    # --- ENCABEZADO IDÉNTICO AL EXCEL ---
    encabezado_table = [
        [Paragraph("<b>MJ LOGISTIC & SYSTEMS E.I.R.L.</b>", style_company), Paragraph(f"<b>PROFORMA: {nro_proforma}</b>", style_proforma)],
        [Paragraph(f"<b>Señores:</b> {cliente}", style_normal), Paragraph(f"<b>Fecha:</b> {fecha}", style_normal)],
        [Paragraph(f"<b>Atención:</b> {atencion}", style_normal), Paragraph(f"<b>Servicio:</b> {tipo_servicio} ({peso_vol})", style_normal)]
    ]
    t_enc = Table(encabezado_table, colWidths=[330, 220])
    t_enc.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP'), ('BOTTOMPADDING', (0,0), (-1,-1), 1)]))
    story.append(t_enc)
    story.append(Spacer(1, 10))
    
    story.append(Paragraph("Por intermedio de la presente nos es grato saludarles y a la vez detallarles nuestra propuesta comercial:", style_normal))
    story.append(Spacer(1, 8))
    
    # --- TABLA 1: COSTOS DE ORIGEN Y FLETE (Fiel a tus celdas) ---
    data_origen = [
        [Paragraph("ORIGEN / FLETE TRÁMITE", style_white), Paragraph("VALOR", style_white), Paragraph("MONEDA", style_white)],
        [Paragraph("FLETE", style_normal), f"{flete:.2f}", "USD"],
        [Paragraph("LOCAL CHARGE", style_normal), f"{local_charge:.2f}", "USD"],
        [Paragraph("<b>TOTAL FLETE</b>", style_bold), f"{total_flete_origen:.2f}", "USD"],
        [Paragraph("TOTAL EXW", style_normal), f"{total_exw:.2f}", "USD"],
        [Paragraph("<b>TOTAL ORIGEN</b>", style_bold), f"{total_origen:.2f}", "USD"]
    ]
    t_orig = Table(data_origen, colWidths=[350, 100, 100])
    t_orig.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1F4E79')), # Azul corporativo oscuro
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#BDC3C7')),
        ('ALIGN', (1,1), (1,-1), 'RIGHT'),
        ('ALIGN', (2,1), (2,-1), 'CENTER'),
        ('BACKGROUND', (0,3), (-1,3), colors.HexColor('#F2F4F4')),
        ('BACKGROUND', (0,5), (-1,5), colors.HexColor('#EAEDED')),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_orig)
    story.append(Spacer(1, 10))
    
    # --- TABLA 2: GASTOS EN DESTINO ---
    data_destino = [
        [Paragraph("GASTO LOCAL EN DESTINO", style_white), Paragraph("MONTO", style_white), Paragraph("ESTADO / REF.", style_white)]
    ]
    for g in st.session_state.gastos_destino:
        data_destino.append([Paragraph(g["concepto"], style_normal), f"{g['monto']:.2f}", Paragraph(g["ref"], style_normal)])
    data_destino.append([Paragraph("<b>TOTAL GAST. LOCAL</b>", style_bold), f"{total_gastos_locales:.2f}", "INCL. IGV"])
    
    t_dest = Table(data_destino, colWidths=[350, 100, 100])
    t_dest.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1E8449')), # Verde corporativo del Excel
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#BDC3C7')),
        ('ALIGN', (1,1), (1,-1), 'RIGHT'),
        ('BACKGROUND', (0,-1), (-1,-1), colors.HexColor('#E8F8F5')),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_dest)
    story.append(Spacer(1, 10))
    
    # --- TABLA 3: IMPUESTOS Y ADUANA ---
    data_impuestos = [
        [Paragraph("IMPUESTOS + PERCEPCIÓN (REFERENCIAL ADUANA)", style_white), "", ""],
        [Paragraph(f"FOB: {fob:.2f} S/", style_normal), Paragraph(f"FLETE APROX: {flete_aprox:.2f} S/", style_normal), Paragraph(f"IGV IMP: {igv_imp:.2f} S/", style_normal)],
        [Paragraph(f"PERCEPCIÓN: {percepcion:.2f} S/", style_normal), Paragraph("<b>VALOR REF S/.</b>", style_bold), Paragraph(f"<b>{(fob+flete_aprox):.2f}</b>", style_bold)],
        [Paragraph("<b>TOTAL ESTIMADO A PAGAR</b>", style_bold), f"<b>{(total_origen + total_gastos_locales):.2f}</b>", "USD"]
    ]
    t_imp = Table(data_impuestos, colWidths=[230, 160, 160])
    t_imp.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#7D6608')), # Marrón / Dorado de aduanas
        ('SPAN', (0,0), (2,0)),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#BDC3C7')),
        ('BACKGROUND', (0,-1), (-1,-1), colors.HexColor('#FDEDEC')),
        ('ALIGN', (1,3), (1,3), 'RIGHT'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_imp)
    
    # CONSTRUIR DOCUMENTO
    doc.build(story)
    buffer.seek(0)
    
    st.download_button(
        label="📥 Descargar Proforma en PDF (1 Hoja)",
        data=buffer,
        file_name=f"PROFORMA_{nro_proforma}.pdf",
        mime="application/pdf"
    )
    st.success("¡PDF optimizado para una sola hoja listo!")
