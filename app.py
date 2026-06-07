import streamlit as st
import io

# Intentar importar WeasyPrint (si ya está en requirements)
try:
    from weasyprint import HTML
    WEASYPRINT_AVAILABLE = True
except ImportError:
    WEASYPRINT_AVAILABLE = False

st.set_page_config(page_title="MJ LOGISTIC - Motor Avanzado PDF", layout="centered")

st.title("💼 Generador de Proformas - Motor de Alta Fidelidad")
st.write("Este sistema utiliza HTML5 y CSS3 para renderizar un PDF con acabado gráfico profesional idéntico al diseño original.")

if not WEASYPRINT_AVAILABLE:
    st.warning("⚠️ El motor avanzado 'WeasyPrint' se está configurando en el servidor. Asegúrate de actualizar tu archivo 'requirements.txt'.")

# 1. CAPTURA DE DATOS DESDE EL CELULAR
st.subheader("📝 Información de la Proforma")
col1, col2 = st.columns(2)
with col1:
    nro_proforma = st.text_input("Número de Proforma", value="MJ240114")
    cliente = st.text_input("Señores (Cliente)", value="ENERGY AND SOLUTIONS ELECTRICAL SAC")
    atencion = st.text_input("Atención", value="Srta. Encargada")
with col2:
    fecha = st.date_input("Fecha de Emisión")
    tipo_servicio = st.text_input("Tipo de Servicio", value="LCL MARITIMO")
    peso_vol = st.text_input("Peso / Volumen", value="1 kl/vol")

st.subheader("💵 Costos Origen y Flete (USD)")
col3, col4, col5 = st.columns(3)
with col3:
    flete = st.number_input("FLETE", value=5.0)
with col4:
    local_charge = st.number_input("LOCAL CHARGE", value=130.0)
with col5:
    total_exw = st.number_input("TOTAL EXW", value=30.0)

# Cálculos matemáticos
total_flete = flete + local_charge
total_origen = total_flete + total_exw

# 2. PLANTILLA VISUAL AVANZADA EN HTML + CSS
html_template = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
    @page {{
        size: A4;
        margin: 15mm;
    }}
    body {{
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        color: #333;
        font-size: 12px;
        line-height: 1.4;
    }}
    .header-table {{
        width: 100%;
        margin-bottom: 20px;
        border-collapse: collapse;
    }}
    .company-name {{
        font-size: 18px;
        font-weight: bold;
        color: #0B2447;
    }}
    .proforma-title {{
        font-size: 16px;
        font-weight: bold;
        text-align: right;
        color: #1F4E79;
    }}
    .intro-text {{
        margin-bottom: 15px;
        font-size: 12px;
    }}
    .data-table {{
        width: 100%;
        border-collapse: collapse;
        margin-bottom: 15px;
    }}
    .data-table th {{
        background-color: #1F4E79;
        color: white;
        font-weight: bold;
        text-align: center;
        padding: 6px;
        font-size: 11px;
        border: 1px solid #BDC3C7;
    }}
    .data-table td {{
        padding: 6px;
        border: 1px solid #BDC3C7;
    }}
    .text-right {{ text-align: right; }}
    .text-center {{ text-align: center; }}
    .row-highlight {{ background-color: #F2F4F4; font-weight: bold; }}
    .row-total {{ background-color: #EAEDED; font-weight: bold; }}
</style>
</head>
<body>

    <table class="header-table">
        <tr>
            <td class="company-name">MJ LOGISTIC & SYSTEMS E.I.R.L.</td>
            <td class="proforma-title">PROFORMA {nro_proforma}</td>
        </tr>
        <tr>
            <td><strong>Señores:</strong> {cliente}</td>
            <td class="text-right"><strong>Fecha:</strong> {fecha}</td>
        </tr>
        <tr>
            <td><strong>Atención:</strong> {atencion}</td>
            <td class="text-right"><strong>Servicio:</strong> {tipo_servicio} ({peso_vol})</td>
        </tr>
    </table>

    <div class="intro-text">
        Por intermedio de la presente nos es grato saludarles y a la vez detallarles nuestra propuesta comercial:
    </div>

    <table class="data-table">
        <thead>
            <tr>
                <th>ORIGEN / FLETE TRÁMITE</th>
                <th style="width: 120px;">VALOR</th>
                <th style="width: 100px;">MONEDA</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>FLETE</td>
                <td class="text-right">{flete:.2f}</td>
                <td class="text-center">USD</td>
            </tr>
            <tr>
                <td>LOCAL CHARGE</td>
                <td class="text-right">{local_charge:.2f}</td>
                <td class="text-center">USD</td>
            </tr>
            <tr class="row-highlight">
                <td>TOTAL FLETE</td>
                <td class="text-right">{total_flete:.2f}</td>
                <td class="text-center">USD</td>
            </tr>
            <tr>
                <td>TOTAL EXW</td>
                <td class="text-right">{total_exw:.2f}</td>
                <td class="text-center">USD</td>
            </tr>
            <tr class="row-total">
                <td>TOTAL ORIGEN</td>
                <td class="text-right">{total_origen:.2f}</td>
                <td class="text-center">USD</td>
            </tr>
        </tbody>
    </table>

</body>
</html>
"""

# BOTÓN DE ACCIÓN
if WEASYPRINT_AVAILABLE:
    if st.button("🚀 Renderizar PDF con Calidad Web Profesional"):
        pdf_file = HTML(string=html_template).write_pdf()
        
        st.download_button(
            label="📥 Descargar PDF Premium de 1 Hoja",
            data=pdf_file,
            file_name=f"PROFORMA_{nro_proforma}.pdf",
            mime="application/pdf"
        )
        st.success("¡Documento procesado con el motor de alta fidelidad!")
