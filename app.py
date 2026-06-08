import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="MJ LOGISTIC - Editor Total", layout="wide")
st.title("💼 Generador de Proformas - Editor Total")

archivo_subido = st.file_uploader("📂 Selecciona tu archivo Excel (.xlsx):", type=["xlsx"])

if archivo_subido:
    # 1. LEER EL EXCEL COMPLETO
    df = pd.read_excel(archivo_subido)
    
    st.info("💡 Edita la tabla abajo, agrega filas o borra lo que necesites.")
    
    # 2. TABLA EDITABLE (Esto es lo que permite modificar todo)
    # Aquí el usuario puede editar, borrar y agregar filas directamente
    df_editado = st.data_editor(df, num_rows="dynamic", use_container_width=True)
    
    # 3. GUARDADO FORZADO
    if st.button("🚀 GRABAR TODOS LOS CAMBIOS"):
        # Convertimos la tabla editada a un archivo Excel en memoria
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df_editado.to_excel(writer, index=False)
            
        st.session_state.archivo_generado = output.getvalue()
        st.success("✅ ¡Cambios grabados correctamente!")

    if 'archivo_generado' in st.session_state:
        st.download_button(
            label="📥 Descargar Excel Actualizado",
            data=st.session_state.archivo_generado,
            file_name="Proforma_Final_Actualizada.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
