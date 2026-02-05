import streamlit as st
from docxtpl import DocxTemplate
import io
import os
import subprocess

st.set_page_config(page_title="Generador de Contratos 2026", page_icon="📝")

st.title("📝 Generador de Contratos (Word & PDF)")
st.info("Sube tu plantilla .docx con etiquetas como {{ nombre_colaborador }} y {{ fecha_contrato }}")

# 1. Cargador de la plantilla
uploaded_file = st.file_uploader("Sube tu plantilla Word (.docx)", type=["docx"])

if uploaded_file:
    # Formulario de entrada de datos
    with st.form("datos_contrato"):
        st.subheader("Información para personalizar")
        
        col1, col2 = st.columns(2)
        with col1:
            nombre = st.text_input("Nombre del Colaborador")
            cedula = st.text_input("Número de Cédula/ID")
        with col2:
            cargo = st.text_input("Cargo a desempeñar")
            # Cambiado de date_input a text_input como solicitaste
            fecha_texto = st.text_input("Fecha del contrato (ej: 5 de febrero de 2026)")
        
        submit = st.form_submit_button("Generar Archivos")

    if submit:
        if not nombre or not fecha_texto:
            st.error("Por favor completa el nombre y la fecha del contrato.")
        else:
            try:
                # 2. Procesar el Word
                doc = DocxTemplate(uploaded_file)
                
                # Diccionario con los datos (asegúrate que coincidan con tu Word)
                contexto = {
                    "nombre_colaborador": nombre,
                    "cedula": cedula,
                    "cargo": cargo,
                    "fecha_contrato": fecha_texto  # Ahora es el texto que ingresaste
                }
                
                doc.render(contexto)
                
                # Guardar temporalmente
                nombre_base = f"Contrato_{nombre.replace(' ', '_')}"
                docx_temp = f"{nombre_base}.docx"
                doc.save(docx_temp)

                st.success("¡Documento procesado correctamente!")

                # --- BOTÓN DESCARGA WORD ---
                with open(docx_temp, "rb") as f:
                    st.download_button(
                        label="📥 Descargar en Word",
                        data=f,
                        file_name=docx_temp,
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                    )

                # --- CONVERSIÓN Y BOTÓN PDF ---
                st.write("Preparando versión PDF...")
                # Este comando requiere LibreOffice (configurado en packages.txt)
                subprocess.run(
                    ['libreoffice', '--headless', '--convert-to', 'pdf', docx_temp],
                    check=True
                )
                
                pdf_temp = docx_temp.replace(".docx", ".pdf")
                
                if os.path.exists(pdf_temp):
                    with open(pdf_temp, "rb") as f_pdf:
                        st.download_button(
                            label="📥 Descargar en PDF",
                            data=f_pdf,
                            file_name=pdf_temp,
                            mime="application/pdf"
                        )
                    
                    # Limpiar archivos del servidor después de la descarga
                    os.remove(docx_temp)
                    os.remove(pdf_temp)

            except Exception as e:
                st.error(f"Hubo un error: {e}")
                st.info("Nota: Para descargar en PDF en la web, asegúrate de tener el archivo 'packages.txt' en tu GitHub.")