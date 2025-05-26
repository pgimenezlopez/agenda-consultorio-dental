import streamlit as st
from pacientes import agregar_paciente, obtener_pacientes, exportar_pacientes_excel
from turnos import agendar_turno, obtener_turnos, exportar_turnos_excel
from db import crear_tablas
import plotly.express as px
import pandas as pd
import base64
from datetime import datetime
from usuarios import USUARIOS

def login():
    st.markdown("## 🔐 Iniciar sesión")
    usuario = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")
    if st.button("Ingresar"):
        if usuario in USUARIOS and USUARIOS[usuario]["password"] == password:
            st.session_state["logueado"] = True
            st.session_state["usuario"] = usuario
            st.rerun()
        else:
            st.error("Usuario o contraseña incorrectos")


if "logueado" not in st.session_state:
    st.session_state["logueado"] = False

if not st.session_state["logueado"]:
    login()
    st.stop()


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
        agregar_paciente(nombre, telefono, observaciones)
        st.success(f"Paciente '{nombre}' guardado correctamente.")

st.divider()

# ------------------- Agendamiento de turnos -------------------

st.markdown("### 📆 Agendamiento de Turnos")

df_pacientes = obtener_pacientes()
st.subheader("📋 Listado de pacientes")
st.dataframe(df_pacientes, use_container_width=True)

st.subheader("📆 Agendar nuevo turno")

nombres = df_pacientes["nombre"].tolist()

with st.form("form_turno"):
    paciente_seleccionado = st.selectbox("Paciente", nombres)
    fecha = st.date_input("Fecha")
    hora = st.time_input("Hora")
    motivo = st.text_input("Motivo")
    submit_turno = st.form_submit_button("🗓️ Guardar turno")

    if submit_turno and paciente_seleccionado:
        paciente_row = df_pacientes[df_pacientes["nombre"] == paciente_seleccionado]
        if not paciente_row.empty:
            paciente_id = int(paciente_row.iloc[0]["id"])
            agendar_turno(paciente_id, str(fecha), str(hora), motivo)
            st.success(f"Turno agendado para {paciente_seleccionado} el {fecha} a las {hora}.")
        else:
            st.error("No se encontró el paciente seleccionado.")

st.divider()

# ------------------- Turnos agendados -------------------

st.markdown("### 🗓️ Turnos Agendados")
df_turnos = obtener_turnos()
st.dataframe(df_turnos, use_container_width=True)

st.divider()

# ------------------- Vista tipo calendario semanal -------------------

st.markdown("### 📊 Vista Semanal (Calendario)")

df_vista = obtener_turnos()

if not df_vista.empty:
    df_vista["start"] = df_vista.apply(lambda row: f"{row['fecha']} {row['hora']}", axis=1)
    df_vista["start"] = pd.to_datetime(df_vista["start"])
    df_vista["end"] = df_vista["start"] + pd.Timedelta(minutes=30)  # duración de 30 min

    fig = px.timeline(
        df_vista,
        x_start="start",
        x_end="end",
        y="nombre",
        color="motivo",
        title="Turnos Semanales",
        labels={"nombre": "Paciente"},
    )
    fig.update_yaxes(autorange="reversed")
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("No hay turnos agendados para mostrar.")

st.divider()

# ------------------- Exportación -------------------

st.markdown("### ⬇️ Exportación de Datos")

def descargar_excel(path, nombre_visible):
    with open(path, "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode()
    href = f'<a href="data:application/octet-stream;base64,{b64}" download="{nombre_visible}">📥 Descargar {nombre_visible}</a>'
    return href

if st.button("📥 Exportar pacientes a Excel", use_container_width=True):
    archivo = exportar_pacientes_excel()
    st.markdown(descargar_excel(archivo, "pacientes.xlsx"), unsafe_allow_html=True)

if st.button("📥 Exportar turnos a Excel", use_container_width=True):
    archivo = exportar_turnos_excel()
    st.markdown(descargar_excel(archivo, "turnos.xlsx"), unsafe_allow_html=True)

if st.button("Cerrar sesión"):
    st.session_state["logueado"] = False
    st.rerun()
