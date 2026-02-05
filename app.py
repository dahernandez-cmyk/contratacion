import streamlit as st
from docxtpl import DocxTemplate
import os
import subprocess
import tempfile

st.set_page_config(page_title="Generador 2026", page_icon="📄")

# Inicializar estados para que los botones no desaparezcan
if 'docx_ready' not in st.session_state:
    st.session_state.docx_ready = None
if 'pdf_ready' not in st.session_state:
    st.session_state.pdf_ready = None
if 'file_name' not in st.session_state:
    st.session_state.file_name = ""

st.title("📄 Generador Pro: Word y PDF")
st.markdown("Sube tu plantilla y genera ambos formatos sin que se borren al descargar.")

uploaded_file = st.file_uploader("Sube tu plantilla Word (.docx)", type=["docx"])

if uploaded_file:
    with st.form("formulario_datos"):
        col1, col2 = st.columns(2)
        with col1:
            nombre = st.text_input("Nombre Completo")
            cedula = st.text_input("Cédula / ID")
        with col2:
            cargo = st.text_input("Cargo")
            fecha_texto = st.text_input("Fecha (ej: 5 de febrero de 2026)")
        
        submit = st.form_submit_button("Generar Documentos")

    if submit:
        if not nombre or not fecha_texto:
            st.error("⚠️ Nombre y Fecha son obligatorios.")
        else:
            try:
                # 1. Procesar Word
                doc = DocxTemplate(uploaded_file)
                contexto = {
                    "nombre_colaborador": nombre,
                    "cedula": cedula,
                    "cargo": cargo,
                    "fecha_contrato": fecha_texto
                }
                doc.render(contexto)

                # 2. Guardar en bytes para persistencia en sesión
                buffer_docx = tempfile.NamedTemporaryFile(delete=False, suffix=".docx")
                doc.save(buffer_docx.name)
                
                with open(buffer_docx.name, "rb") as f:
                    st.session_state.docx_ready = f.read()

                # 3. Convertir a PDF usando LibreOffice
                st.write("Convirtiendo a PDF...")
                output_dir = tempfile.gettempdir()
                subprocess.run([
                    'libreoffice', '--headless', 
                    '-env:UserInstallation=file:///tmp/libo_user_profile',
                    '--convert-to', 'pdf', 
                    '--outdir', output_dir, 
                    buffer_docx.name
                ], check=True)

                pdf_path = buffer_docx.name.replace(".docx", ".pdf")
                
                with open(pdf_path, "rb") as f:
                    st.session_state.pdf_ready = f.read()
                
                st.session_state.file_name = nombre.replace(" ", "_")
                st.success("✅ ¡Archivos generados!")

                # Limpiar archivos temporales del disco
                os.remove(buffer_docx.name)
                os.remove(pdf_path)

            except Exception as e:
                st.error(f"Error: {e}")

    # Mostrar botones de descarga si los datos están en sesión
    if st.session_state.docx_ready and st.session_state.pdf_ready:
        st.divider()
        st.subheader("Descargas Disponibles:")
        c1, c2 = st.columns(2)
        
        c1.download_button(
            label="📥 Descargar Word",
            data=st.session_state.docx_ready,
            file_name=f"Contrato_{st.session_state.file_name}.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
        
        c2.download_button(
            label="📥 Descargar PDF",
            data=st.session_state.pdf_ready,
            file_name=f"Contrato_{st.session_state.file_name}.pdf",
            mime="application/pdf"
        )