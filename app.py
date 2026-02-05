import streamlit as st
from docxtpl import DocxTemplate
import io
import os
import subprocess

st.set_page_config(page_title="Generador de Documentos 2026", page_icon="📄")

st.title("📄 Generador de Documentos (Word & PDF)")
st.info("Sube una plantilla .docx con etiquetas tipo {{ nombre_colaborador }}")

# 1. Cargador de archivos
uploaded_file = st.file_uploader("Sube tu plantilla Word", type=["docx"])

if uploaded_file:
    # Formulario de datos
    with st.form("datos"):
        col1, col2 = st.columns(2)
        with col1:
            nombre = st.text_input("Nombre del Colaborador")
            cedula = st.text_input("Cédula/ID")
        with col2:
            cargo = st.text_input("Cargo")
            fecha = st.text_input("Fecha del documento")
        
        submit = st.form_submit_button("Procesar Documento")

    if submit:
        if not nombre:
            st.error("El nombre es obligatorio.")
        else:
            # 2. Generar el Word en memoria
            doc = DocxTemplate(uploaded_file)
            contexto = {
                "nombre_colaborador": nombre,
                "cedula": cedula,
                "cargo": cargo,
                "fecha": fecha.strftime("%d/%m/%Y")
            }
            doc.render(contexto)
            
            # Guardar temporalmente para Word y conversión
            nombre_temp_docx = f"temp_{nombre}.docx"
            doc.save(nombre_temp_docx)

            # --- SECCIÓN DE DESCARGA WORD ---
            with open(nombre_temp_docx, "rb") as f:
                st.download_button(
                    label="📥 Descargar en Word",
                    data=f,
                    file_name=f"Documento_{nombre}.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )

            # --- SECCIÓN DE CONVERSIÓN A PDF ---
            try:
                st.write("Generando PDF... por favor espera.")
                # Comando para LibreOffice (Funciona en Streamlit Cloud con el archivo packages.txt)
                subprocess.run(
                    ['libreoffice', '--headless', '--convert-to', 'pdf', nombre_temp_docx],
                    check=True
                )
                
                nombre_temp_pdf = nombre_temp_docx.replace(".docx", ".pdf")
                
                if os.path.exists(nombre_temp_pdf):
                    with open(nombre_temp_pdf, "rb") as pdf_file:
                        st.download_button(
                            label="📥 Descargar en PDF",
                            data=pdf_file,
                            file_name=f"Documento_{nombre}.pdf",
                            mime="application/pdf"
                        )
                    # Limpieza de archivos temporales
                    os.remove(nombre_temp_docx)
                    os.remove(nombre_temp_pdf)
                
            except Exception as e:
                st.error(f"Error al generar PDF: {e}")
                st.warning("Nota: La descarga PDF requiere LibreOffice instalado en el sistema.")