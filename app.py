import streamlit as st
from docxtpl import DocxTemplate
import io

st.set_page_config(page_title="Otrosí Habeas Data", layout="centered")

st.title("📄 Otrosí Autorización Habeas Data")
st.write("Sube tu plantilla y completa los datos.")

# 1. Cargar la plantilla
uploaded_file = st.file_uploader("Elige tu archivo Word (.docx)", type=["docx"])

if uploaded_file:
    # Leer la plantilla desde el archivo subido
    doc = DocxTemplate(uploaded_file)
    
    # Obtener las variables de la plantilla (opcional, pero ayuda al usuario)
    st.info("Asegúrate de que tu Word tenga etiquetas como `{{ nombre_colaborador }}`")
    
    with st.form("datos_formulario"):
        st.subheader("Datos del Colaborador")
        nombre = st.text_input("Nombre del Colaborador")
        cedula = st.text_input("Cédula o ID")
        cargo = st.text_input("Cargo")
        fecha_contrato = st.text_input("Fecha Contrato")
        
        # Botón para procesar
        submit = st.form_submit_button("Generar Documento")

    if submit:
        if nombre and cedula:
            # 2. Definir el contexto para reemplazar
            contexto = {
                "nombre_colaborador": nombre,
                "cedula": cedula,
                "cargo": cargo,
                "fecha_contrato": fecha_contrato
            }
            
            # 3. Renderizar cambios
            doc.render(contexto)
            
            # 4. Guardar en memoria para descarga
            output = io.BytesIO()
            doc.save(output)
            output.seek(0)
            
            st.success("✅ ¡Documento generado con éxito!")
            st.download_button(
                label="📥 Descargar archivo personalizado",
                data=output,
                file_name=f"Documento_{nombre}.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )
        else:
            st.error("Por favor, completa al menos el nombre y la cédula.")