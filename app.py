import streamlit as st
from pacientes import agregar_paciente, obtener_pacientes, exportar_pacientes_excel
from turnos import agendar_turno, obtener_turnos, exportar_turnos_excel
from db import crear_tablas
import plotly.express as px
import pandas as pd
import base64
from datetime import datetime

# Configuración de página
st.set_page_config(
    page_title="Agenda Dental",
    page_icon="🦷",
    layout="wide",
    initial_sidebar_state="expanded"
)

crear_tablas()

# ------------------- Gestión de pacientes -------------------

st.markdown("### 👤 Gestión de Pacientes")

with st.form("form_paciente"):
    col1, col2 = st.columns(2)
    with col1:
        nombre = st.text_input("Nombre del paciente")
    with col2:
        telefono = st.text_input("Teléfono")

    observaciones = st.text_area("Observaciones")

    submit_paciente = st.form_submit_button("💾 Guardar paciente")

    if submit_paciente and nombre:
        agregar_paciente(nomb_
