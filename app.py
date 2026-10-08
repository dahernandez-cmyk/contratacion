import streamlit as st
from docxtpl import DocxTemplate
import os
import subprocess
import tempfile

st.set_page_config(page_title="Generador Documental", page_icon="📄")

# --- 1. CONFIGURACIÓN MAESTRA DE CAMPOS ---
# Cada contrato es un mundo aparte aquí.
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
            "Celular":"Celular_colaborador",
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
            "Celular":"Celular_colaborador",
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
            "Celular":"Celular_colaborador",
            "Cargo": "Cargo",
            "Salario Letra": "Salario_Letra",
            "Salario Número": "Salario_numero",
            "Fecha de Ingreso": "Fecha_de_ingreso",
            "Periodo de Prueba":"Periodo_de_Prrueba",
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
            "Celular":"Celular_colaborador",
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
            "Celular":"Celular_colaborador",
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
            "Contacto de Emergencia":"Nombre_contacto_emergencia",
            "Parentesco":"Nombre_contacto_emergencia2",
            "Correo": "Correo",
            "Celular":"Celular_colaborador",
            "Cargo": "Cargo",
            "Líder":"Lider",
            "Centro de Costo":"CECO",
            "Detalle y Porcentaje de Obra":"Detalle_y_porcentaje_de_obra",
            "Fecha de Ingreso": "Fecha_de_ingreso",
            "Fecha de Terminación Curso":"Fecha_de_terminacion_cuso",
            "Fecha Ingreso a la obra":"Fecha_de_ingreso_a_obra",
            "ARL":"ARL",
            "EPS":"EPS",
            "AFC":"AFC",
            "AFP":"AFP",
            "Caja de Compensación":"Caja_de_compensacion"
        }
    },
    "Otrosi Auxilio de desplazamiento": {
        "mapping": {
            "Nombre Completo": "Nombre",
            "Cédula": "cedula",
            "Cargo": "Cargo",
            "Fecha de Ingreso": "Fecha_de_ingreso",
            "Fecha Auxilio": "Fecha_Aux",
            "Auxilio Letra":"Aux_Letra",
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
            "Obra":"Obra",
            "Fecha Firma":"Fecha_firma"

        }
    },
    "Otrosi Prima Zonal": {
        "mapping": {
            "Nombre Completo": "Nombre",
            "Cédula": "cedula",
            "Cargo": "Cargo",
            "Prima Zonal Valor": "Valor_numero",
            "Prima Zonal Letra": "Valor_letra",
            "Fecha Firma":"Fecha_firma",
            "Fecha de Ingreso": "Fecha_de_ingreso",
            "Nombre de la obra":"Nombre_de_la_obra"

        }
    },
    "Plantilla entrega dotación operativa": {
        "mapping": {
            "Nombre Completo": "Nombre",
            "Cédula": "cedula",
            "Cargo": "Cargo",
            "Obra":"Obra",
            "Fecha de Ingreso": "Fecha_de_ingreso",
            "Ciudad": "Ciudad"

        }
    }
}

# --- 2. LÓGICA DE SESIÓN ---
if 'docx_ready' not in st.session_state: st.session_state.docx_ready = None
if 'pdf_ready' not in st.session_state: st.session_state.pdf_ready = None

st.title("📄 Generador Multicontratoooo")

# --- 3. SELECCIÓN Y CARGA ---
tipo_contrato = st.selectbox("Seleccione el documento a generar:", list(CONTRATOS.keys()))
archivo_plantilla = st.file_uploader(f"Suba plantilla para {tipo_contrato}", type=["docx"])

if archivo_plantilla:
    # Creamos el formulario dinámico
    with st.form("formulario_dinamico"):
        st.subheader("Complete la información necesaria")
        respuestas_usuario = {}
        
        # Obtenemos los campos específicos de este contrato
        config_actual = CONTRATOS[tipo_contrato]["mapping"]
        
        # Generar inputs basados en las llaves del mapping
        cols = st.columns(2)
        for i, etiqueta_ui in enumerate(config_actual.keys()):
            with cols[i % 2]:
                respuestas_usuario[etiqueta_ui] = st.text_input(etiqueta_ui)
        
        boton_generar = st.form_submit_button("Generar Archivos")

    if boton_generar:
        if any(not val.strip() for val in respuestas_usuario.values()):
            st.warning("⚠️ Por favor rellene todos los campos.")
        else:
            try:
                # 4. PROCESAMIENTO
                doc = DocxTemplate(archivo_plantilla)
                
                # Creamos el contexto final cruzando UI -> Tag de Word
                # Ejemplo: {"nombre_colaborador": "Juan Perez", ...}
                contexto_final = {config_actual[k]: v for k, v in respuestas_usuario.items()}
                
                doc.render(contexto_final)

                # Guardado temporal
                with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp_docx:
                    doc.save(tmp_docx.name)
                    path_docx = tmp_docx.name
                
                # Conversión a PDF
                st.info("Convertiendo...")
                out_dir = tempfile.gettempdir()
                subprocess.run([
                    'libreoffice', '--headless', 
                    '-env:UserInstallation=file:///tmp/libo_user_profile',
                    '--convert-to', 'pdf', '--outdir', out_dir, path_docx
                ], check=True)

                path_pdf = path_docx.replace(".docx", ".pdf")

                # Guardar en sesión para descarga
                with open(path_docx, "rb") as f: st.session_state.docx_ready = f.read()
                with open(path_pdf, "rb") as f: st.session_state.pdf_ready = f.read()
                
                st.success("✅ Documentos generados.")
                
                # Limpiar disco
                os.remove(path_docx)
                os.remove(path_pdf)

            except Exception as e:
                st.error(f"Error: {e}")

# --- 5. DESCARGAS ---
if st.session_state.docx_ready:
    st.divider()
    c1, c2 = st.columns(2)
    c1.download_button("📥 Descargar Word", st.session_state.docx_ready, "documento.docx")
    c2.download_button("📥 Descargar PDF", st.session_state.pdf_ready, "documento.pdf")