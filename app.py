import streamlit as st
from docxtpl import DocxTemplate
import io

st.title("Generador de Documentos desde Word")

# 1. Entrada de datos
nombre = st.text_input("Nombre del Colaborador")
id_colaborador = st.text_input("Cédula/ID")

if st.button("Generar Documento"):
    # 2. Cargar la plantilla .docx
    # Asegúrate de que 'plantilla.docx' esté en la misma carpeta
    doc = DocxTemplate("plantilla.docx")
    
    # 3. Definir qué reemplazar (Diccionario de contexto)
    contexto = {
        "nombre_colaborador": nombre,
        "cedula": id_colaborador,
        "fecha": "05 de febrero de 2026" # Podrías usar datetime
    }
    
    # 4. Renderizar (Reemplazar las llaves por los datos)
    doc.render(contexto)
    
    # 5. Guardar en memoria para descarga
    bio = io.BytesIO()
    doc.save(bio)
    bio.seek(0)
    
    st.download_button(
        label="Descargar Word Personalizado",
        data=bio,
        file_name=f"Contrato_{nombre}.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )