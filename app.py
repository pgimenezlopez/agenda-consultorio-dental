import streamlit as st
from pacientes import agregar_paciente, obtener_pacientes
from db import crear_tablas
from turnos import agendar_turno, obtener_turnos
import plotly.express as px
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="Agenda Dental",
    page_icon="🦷",
    layout="wide",
    initial_sidebar_state="expanded"
)

crear_tablas()

st.markdown("### 👤 Gestión de Pacientes")
# Formulario de pacientes

st.subheader("Agregar nuevo paciente")
with st.form("form_paciente"):
    col1, col2 = st.columns(2)
    with col1:
        nombre = st.text_input("Nombre del paciente")
    with col2:
        telefono = st.text_input("Teléfono")

    observaciones = st.text_area("Observaciones")

    submit = st.form_submit_button("💾 Guardar paciente")

    if submitted and nombre:
        agregar_paciente(nombre, telefono, observaciones)
        st.success(f"Paciente '{nombre}' guardado correctamente.")

st.divider()

st.markdown("### 📆 Agendamiento de Turnos")
# Formulario de turnos
st.subheader("Listado de pacientes")
df_pacientes = obtener_pacientes()
st.dataframe(df_pacientes, use_container_width=True)

st.subheader("📆 Agendar turno")

df_pacientes = obtener_pacientes()
nombres = df_pacientes["nombre"].tolist()

with st.form("form_turno"):
    paciente_seleccionado = st.selectbox("Paciente", nombres)
    fecha = st.date_input("Fecha")
    hora = st.time_input("Hora")
    motivo = st.text_input("Motivo")
    submit_turno = st.form_submit_button("Guardar turno")

    if submit_turno and paciente_seleccionado:
        paciente_id = df_pacientes[df_pacientes["nombre"] == paciente_seleccionado]["id"].values[0]
        agendar_turno(paciente_id, str(fecha), str(hora), motivo)
        st.success(f"Turno agendado para {paciente_seleccionado} el {fecha} a las {hora}.")

st.divider()

st.markdown("### 🗓️ Turnos Agendados")
# Tabla de turnos

df_turnos = obtener_turnos()
st.dataframe(df_turnos, use_container_width=True)

from pacientes import exportar_pacientes_excel
from turnos import exportar_turnos_excel
import base64

import plotly.express as px
import pandas as pd
from datetime import datetime

st.divider()

st.markdown("### 📊 Vista Semanal (Calendario)")
# Gráfico Plotly

df_vista = obtener_turnos()

if not df_vista.empty:
    df_vista["start"] = df_vista.apply(lambda row: f"{row['fecha']} {row['hora']}", axis=1)
    df_vista["start"] = pd.to_datetime(df_vista["start"])
    df_vista["end"] = df_vista["start"] + pd.Timedelta(minutes=30)  # asumimos que cada turno dura 30min

    fig = px.timeline(
        df_vista,
        x_start="start",
        x_end="end",
        y="nombre",
        color="motivo",
        title="Turnos Semanales",
        labels={"nombre": "Paciente"},
    )
    fig.update_yaxes(autorange="reversed")  # Ordenar pacientes
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("No hay turnos agendados para mostrar.")


def descargar_excel(path, nombre_visible):
    with open(path, "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode()
    href = f'<a href="data:application/octet-stream;base64,{b64}" download="{nombre_visible}">📥 Descargar {nombre_visible}</a>'
    return href


st.divider()

st.markdown("### ⬇️ Exportación de datos")
# Botones para exportar


if st.button("Exportar pacientes a Excel"):
    archivo = exportar_pacientes_excel()
    st.markdown(descargar_excel(archivo, "pacientes.xlsx"), unsafe_allow_html=True)

if st.button("Exportar turnos a Excel"):
    archivo = exportar_turnos_excel()
    st.markdown(descargar_excel(archivo, "turnos.xlsx"), unsafe_allow_html=True)

