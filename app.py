import streamlit as st
from docxtpl import DocxTemplate
import os
import subprocess
import tempfile

st.set_page_config(page_title="Generador de Contratos 2026", page_icon="📄")

st.title("📄 Generador de Contratos (Word & PDF)")
st.markdown("""
Esta herramienta permite cargar una plantilla Word y generar documentos personalizados.
**Instrucciones:** Su plantilla debe contener etiquetas como `{{ nombre_colaborador }}`, `{{ cedula }}`, `{{ cargo }}` y `{{ fecha_contrato }}`.
""")

# Cargador de la plantilla
uploaded_file = st.file_uploader("Sube tu plantilla Word (.docx)", type=["docx"])

if uploaded_file:
    with st.form("formulario_datos"):
        st.subheader("Información del Colaborador")
        col1, col2 = st.columns(2)
        
        with col1:
            nombre = st.text_input("Nombre Completo")
            cedula = st.text_input("Cédula / ID")
        
        with col2:
            cargo = st.text_input("Cargo")
            fecha_texto = st.text_input("Fecha del contrato (ej: 5 de febrero de 2026)")
        
        submit = st.form_submit_button("Generar Documentos")

    if submit:
        if not nombre or not fecha_texto:
            st.error("⚠️ El nombre y la fecha son obligatorios.")
        else:
            try:
                # Procesar la plantilla con docxtpl
                doc = DocxTemplate(uploaded_file)
                contexto = {
                    "nombre_colaborador": nombre,
                    "cedula": cedula,
                    "cargo": cargo,
                    "fecha_contrato": fecha_texto
                }
                doc.render(contexto)

                # Creamos un entorno temporal para procesar los archivos
                with tempfile.TemporaryDirectory() as tmpdirname:
                    # Definir rutas de archivos
                    docx_path = os.path.join(tmpdirname, f"Contrato_{nombre.replace(' ', '_')}.docx")
                    doc.save(docx_path)

                    # --- OPCIÓN WORD ---
                    with open(docx_path, "rb") as f_word:
                        st.download_button(
                            label="📥 Descargar en Word",
                            data=f_word,
                            file_name=f"Contrato_{nombre}.docx",
                            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                        )

                    # --- PROCESO PDF (LibreOffice) ---
                    st.write("Generando versión PDF...")
                    
                    # El comando incluye un perfil de usuario temporal para evitar errores de permisos
                    # El parámetro --outdir es fundamental para que el PDF quede en la carpeta temporal
                    subprocess.run([
                        'libreoffice', 
                        '--headless', 
                        '-env:UserInstallation=file:///tmp/libo_user_profile',
                        '--convert-to', 'pdf', 
                        '--outdir', tmpdirname, 
                        docx_path
                    ], check=True)

                    pdf_path = docx_path.replace(".docx", ".pdf")

                    # Verificar si el PDF se creó y ofrecer descarga
                    if os.path.exists(pdf_path):
                        with open(pdf_path, "rb") as f_pdf:
                            st.download_button(
                                label="📥 Descargar en PDF",
                                data=f_pdf,
                                file_name=f"Contrato_{nombre}.pdf",
                                mime="application/pdf"
                            )
                        st.success("✅ ¡Archivos listos!")
                    else:
                        st.error("No se pudo localizar el archivo PDF generado.")

            except subprocess.CalledProcessError:
                st.error("Error al convertir a PDF. Verifique que 'libreoffice' esté en su archivo packages.txt.")
            except Exception as e:
                st.error(f"Ocurrió un error inesperado: {e}")