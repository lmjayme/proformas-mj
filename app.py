import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="MJ LOGISTIC - Lector Total", layout="wide")
st.title("💼 Generador de Proformas - Lector Completo")

archivo_subido = st.file_uploader("📂 Selecciona tu archivo CSV o Excel:", type=["csv", "xlsx"])

if archivo_subido:
    # 1. CARGA INTELIGENTE (Detecta si es Excel o CSV)
    try:
        if archivo_subido.name.endswith('.csv'):
            df = pd.read_csv(archivo_subido)
        else:
            df = pd.read_excel(archivo_subido)
        
        st.success("✅ Archivo cargado completamente.")
        
        # 2. MOSTRAR TODO EL CONTENIDO
        st.subheader("📋 Datos del archivo")
        st.dataframe(df, use_container_width=True)
        
        # 3. AQUÍ PODRÍAS EDITAR VALORES ESPECÍFICOS
        st.subheader("✏️ Edición Rápida")
        # Esto permite editar la tabla entera como si fuera un Excel
        df_editado = st.data_editor(df, use_container_width=True)
        
        # 4. BOTÓN PARA DESCARGAR EL NUEVO ARCHIVO
        if st.button("💾 Guardar cambios y Descargar"):
            output = io.BytesIO()
            df_editado.to_csv(output, index=False)
            st.download_button("📥 Descargar CSV editado", output.getvalue(), "Proforma_Editada.csv")
            
    except Exception as e:
        st.error(f"Error al leer el archivo: {e}")
