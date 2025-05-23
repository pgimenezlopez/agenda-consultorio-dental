import streamlit as st
from pacientes import agregar_paciente, obtener_pacientes
from db import crear_tablas
from turnos import agendar_turno, obtener_turnos
import plotly.express as px
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Agenda Dental", layout="centered")
crear_tablas()

st.title("🦷 Gestión de Pacientes")

st.subheader("Agregar nuevo paciente")
with st.form("form_paciente"):
    nombre = st.text_input("Nombre")
    telefono = st.text_input("Teléfono")
    observaciones = st.text_area("Observaciones")
    submitted = st.form_submit_button("Guardar")
    if submitted and nombre:
        agregar_paciente(nombre, telefono, observaciones)
        st.success(f"Paciente '{nombre}' guardado correctamente.")

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

st.subheader("📋 Turnos agendados")
df_turnos = obtener_turnos()
st.dataframe(df_turnos, use_container_width=True)

from pacientes import exportar_pacientes_excel
from turnos import exportar_turnos_excel
import base64

import plotly.express as px
import pandas as pd
from datetime import datetime

st.subheader("📆 Vista semanal de turnos")

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

st.subheader("⬇️ Exportar datos")

if st.button("Exportar pacientes a Excel"):
    archivo = exportar_pacientes_excel()
    st.markdown(descargar_excel(archivo, "pacientes.xlsx"), unsafe_allow_html=True)

if st.button("Exportar turnos a Excel"):
    archivo = exportar_turnos_excel()
    st.markdown(descargar_excel(archivo, "turnos.xlsx"), unsafe_allow_html=True)

