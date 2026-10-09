import streamlit as st
from docxtpl import DocxTemplate
import os
import subprocess
import tempfile
import zipfile

st.set_page_config(page_title="Generador Documental Múltiple", page_icon="📄")

# --- 1. CONFIGURACIÓN MAESTRA DE CAMPOS ---
CONTRATOS = {
    "Otrosí Habeas Data": {
        "mapping": {
            "Nombre Completo": "nombre_colaborador",
            "Cédula": "cedula",
            "Cargo": "cargo",
            "Fecha de Firma": "fecha_contrato"
        }
    },
    "Otrosí Flexitrabajo": {
        "mapping": {
            "Nombre del Empleado": "nombre_colaborador",
            "Cédula": "cedula",
            "Cargo": "cargo",
            "Fecha Contrato": "fecha_contrato"
        }
    },
    "Contrato a término fijo": {
        "mapping": {
            "Nombre Completo": "Nombre",
            "Cédula": "cedula",
            "Dirección": "Dirreccion_Colaborador",
            "Correo": "Correo",
            "Lugar y Fecha de Nacimiento": "lugar_y_fecha_de_nacimiento",
            "Celular": "Celular_colaborador",
            "Cargo": "Cargo",
            "Salario Letra": "Salario_Letra",
            "Salario Número": "Salario_numero",
            "Fecha de Ingreso": "Fecha_de_ingreso",
            "Ciudad": "Ciudad",
            "Duración": "Duracion",
            "Vencimiento": "Vencimiento"
        }
    },
    "Contrato a término fijo inferior a 1 año": {
        "mapping": {
            "Nombre Completo": "Nombre",
            "Cédula": "cedula",
            "Dirección": "Dirreccion_Colaborador",
            "Correo": "Correo",
            "Lugar y Fecha de Nacimiento": "lugar_y_fecha_de_nacimiento",
            "Celular": "Celular_colaborador",
            "Cargo": "Cargo",
            "Salario Letra": "Salario_Letra",
            "Salario Número": "Salario_numero",
            "Fecha de Ingreso": "Fecha_de_ingreso",
            "Ciudad": "Ciudad",
            "Duración": "Duracion",
            "Vencimiento": "Vencimiento"
        }
    },
    "Contrato de obra o labor": {
        "mapping": {
            "Nombre Completo": "Nombre",
            "Cédula": "cedula",
            "Dirección": "Dirreccion_Colaborador",
            "Correo": "Correo",
            "Lugar y Fecha de Nacimiento": "lugar_y_fecha_de_nacimiento",
            "Celular": "Celular_colaborador",
            "Cargo": "Cargo",
            "Salario Letra": "Salario_Letra",
            "Salario Número": "Salario_numero",
            "Fecha de Ingreso": "Fecha_de_ingreso",
            "Periodo de Prueba": "Periodo_de_Prrueba",
            "Ciudad": "Ciudad",
            "Porcentaje de Actividad": "porcentaje_de_actividad",
            "Detalle y Porcentaje de Obra": "Detalle_y_porcentaje_de_obra"
        }
    },
    "Contrato fijo DEI Comercial": {
        "mapping": {
            "Nombre Completo": "Nombre",
            "Cédula": "cedula",
            "Dirección": "Dirreccion_Colaborador",
            "Correo": "Correo",
            "Lugar y Fecha de Nacimiento": "lugar_y_fecha_de_nacimiento",
            "Celular": "Celular_colaborador",
            "Cargo": "Cargo",
            "Salario Letra": "Salario_Letra",
            "Salario Número": "Salario_numero",
            "Fecha de Ingreso": "Fecha_de_ingreso",
            "Ciudad": "Ciudad",
            "Duración": "Duracion",
            "Vencimiento": "Vencimiento"
        }
    },
    "Contrato salario integral": {
        "mapping": {
            "Nombre Completo": "Nombre",
            "Cédula": "cedula",
            "Dirección": "Dirreccion_Colaborador",
            "Correo": "Correo",
            "Lugar y Fecha de Nacimiento": "lugar_y_fecha_de_nacimiento",
            "Celular": "Celular_colaborador",
            "Cargo": "Cargo",
            "Salario Letra": "Salario_Letra",
            "Salario Número": "Salario_numero",
            "Fecha de Ingreso": "Fecha_de_ingreso",
            "Ciudad": "Ciudad"
        }
    },
    "Ficha de ingreso": {
        "mapping": {
            "Nombre Completo": "Nombre",
            "Cédula": "cedula",
            "Dirección": "Dirreccion_Colaborador",
            "Contacto de Emergencia": "Nombre_contacto_emergencia",
            "Parentesco": "Nombre_contacto_emergencia2",
            "Correo": "Correo",
            "Celular": "Celular_colaborador",
            "Cargo": "Cargo",
            "Líder": "Lider",
            "Centro de Costo": "CECO",
            "Detalle y Porcentaje de Obra": "Detalle_y_porcentaje_de_obra",
            "Fecha de Ingreso": "Fecha_de_ingreso",
            "Fecha de Terminación Curso": "Fecha_de_terminacion_cuso",
            "Fecha Ingreso a la obra": "Fecha_de_ingreso_a_obra",
            "ARL": "ARL",
            "EPS": "EPS",
            "AFC": "AFC",
            "AFP": "AFP",
            "Caja de Compensación": "Caja_de_compensacion"
        }
    },
    "Otrosi Auxilio de desplazamiento": {
        "mapping": {
            "Nombre Completo": "Nombre",
            "Cédula": "cedula",
            "Cargo": "Cargo",
            "Fecha de Ingreso": "Fecha_de_ingreso",
            "Fecha Auxilio": "Fecha_Aux",
            "Auxilio Letra": "Aux_Letra",
            "Auxilio Número": "Aux_numero"
        }
    },
    "Otrosi Auxilios Varios": {
        "mapping": {
            "Nombre Completo": "Nombre",
            "Cédula": "cedula",
            "Cargo": "Cargo",
            "Fecha de Ingreso": "Fecha_de_ingreso",
            "Valor Auxilio Alimentación": "Valor_numero_A",
            "Valor Auxilio Desplazamiento": "Valor_numero_D",
            "Valor Auxilio Vivienda": "Valor_numero_V",
            "Obra": "Obra",
            "Fecha Firma": "Fecha_firma"
        }
    },
    "Otrosi Prima Zonal": {
        "mapping": {
            "Nombre Completo": "Nombre",
            "Cédula": "cedula",
            "Cargo": "Cargo",
            "Prima Zonal Valor": "Valor_numero",
            "Prima Zonal Letra": "Valor_letra",
            "Fecha Firma": "Fecha_firma",
            "Fecha de Ingreso": "Fecha_de_ingreso",
            "Nombre de la obra": "Nombre_de_la_obra"
        }
    },
    "Plantilla entrega dotación operativa": {
        "mapping": {
            "Nombre Completo": "Nombre",
            "Cédula": "cedula",
            "Cargo": "Cargo",
            "Obra": "Obra",
            "Fecha de Ingreso": "Fecha_de_ingreso",
            "Ciudad": "Ciudad"
        }
    }
}

# --- 2. LÓGICA DE SESIÓN ---
if 'zip_ready' not in st.session_state: 
    st.session_state.zip_ready = None

st.title("📄 Generador Multicontrato")

# --- 3. SELECCIÓN DE CONTRATOS Y PLANTILLAS ---
contratos_seleccionados = st.multiselect(
    "Seleccione los documentos a generar:", 
    list(CONTRATOS.keys())
)

archivos_plantillas = {}
if contratos_seleccionados:
    st.subheader("Suba las plantillas requeridas:")
    cols_up = st.columns(min(len(contratos_seleccionados), 3))
    for idx, contrato in enumerate(contratos_seleccionados):
        with cols_up[idx % 3]:
            archivos_plantillas[contrato] = st.file_uploader(
                f"Plantilla: {contrato}", 
                type=["docx"], 
                key=f"file_{contrato}"
            )

# Verificar si todas las plantillas han sido subidas
todas_plantillas_listas = (
    len(contratos_seleccionados) > 0 and 
    all(archivos_plantillas.get(c) is not None for c in contratos_seleccionados)
)

if todas_plantillas_listas:
    # --- 4. CONSOLIDACIÓN DE CAMPOS DEL FORMULARIO ---
    # Unificamos todas las etiquetas visuales para mostrarlas una sola vez
    etiquetas_unicas = list(dict.fromkeys(
        etiqueta 
        for contrato in contratos_seleccionados 
        for etiqueta in CONTRATOS[contrato]["mapping"].keys()
    ))

    with st.form("formulario_consolidado"):
        st.subheader("Complete los datos requeridos")
        st.caption("Los campos comunes solo se solicitan una vez y se aplicarán a todos los contratos seleccionados.")
        
        respuestas_usuario = {}
        cols = st.columns(2)
        
        # Generar campos únicos
        for i, etiqueta_ui in enumerate(etiquetas_unicas):
            with cols[i % 2]:
                respuestas_usuario[etiqueta_ui] = st.text_input(etiqueta_ui)
        
        boton_generar = st.form_submit_button("Generar Todos los Documentos")

    # --- 5. PROCESAMIENTO MÚLTIPLE ---
    if boton_generar:
        if any(not val.strip() for val in respuestas_usuario.values()):
            st.warning("⚠️ Por favor rellene todos los campos.")
        else:
            try:
                st.info("Generando y convirtiendo documentos...")
                
                # Directorio temporal para los resultados
                with tempfile.TemporaryDirectory() as temp_dir:
                    docx_paths = []
                    pdf_paths = []

                    for idx, contrato in enumerate(contratos_seleccionados):
                        plantilla = archivos_plantillas[contrato]
                        config_actual = CONTRATOS[contrato]["mapping"]
                        
                        # Armar contexto específico para este contrato
                        contexto_contrato = {
                            var_word: respuestas_usuario[etiqueta_ui]
                            for etiqueta_ui, var_word in config_actual.items()
                        }
                        
                        # Renderizar Word
                        doc = DocxTemplate(plantilla)
                        doc.render(contexto_contrato)
                        
                        # Nombre seguro de archivo
                        nombre_base = f"{idx+1}_{contrato.replace(' ', '_')}"
                        path_docx = os.path.join(temp_dir, f"{nombre_base}.docx")
                        doc.save(path_docx)
                        docx_paths.append(path_docx)

                        # Conversión individual a PDF con LibreOffice
                        subprocess.run([
                            'libreoffice', '--headless', 
                            '-env:UserInstallation=file:///tmp/libo_user_profile',
                            '--convert-to', 'pdf', '--outdir', temp_dir, path_docx
                        ], check=True)

                        path_pdf = os.path.join(temp_dir, f"{nombre_base}.pdf")
                        pdf_paths.append(path_pdf)

                    # Crear paquete ZIP con todos los DOCX y PDF
                    zip_path = os.path.join(temp_dir, "documentos_generados.zip")
                    with zipfile.ZipFile(zip_path, 'w') as zipf:
                        for f in docx_paths + pdf_paths:
                            zipf.write(f, os.path.basename(f))

                    # Guardar archivo ZIP en st.session_state
                    with open(zip_path, "rb") as z:
                        st.session_state.zip_ready = z.read()

                st.success("✅ ¡Todos los documentos se generaron con éxito!")

            except Exception as e:
                st.error(f"Error procesando los documentos: {e}")

elif contratos_seleccionados:
    st.info("📌 Por favor suba las plantillas de todos los contratos seleccionados para ver el formulario.")

# --- 6. DESCARGA PAQUETE COMPLETO ---
if st.session_state.zip_ready:
    st.divider()
    st.download_button(
        label="📥 Descargar todos los documentos (.ZIP)",
        data=st.session_state.zip_ready,
        file_name="paquete_documentos.zip",
        mime="application/zip",
        use_container_width=True
    )