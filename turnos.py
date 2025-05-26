import pandas as pd
from supabase_config import supabase


def agendar_turno(paciente_id, fecha, hora, motivo, profesional):
    supabase.table("turnos").insert({
        "paciente_id": paciente_id,
        "fecha": fecha,
        "hora": hora,
        "motivo": motivo,
        "profesional": profesional
    }).execute()


def obtener_turnos(profesional=None):
    query = supabase.table("turnos").select("id, fecha, hora, motivo, profesional, pacientes(nombre)")
    if profesional:
        query = query.eq("profesional", profesional)
    response = query.execute()

    data = response.data or []

    # Normalizamos pacientes.nombre desde la relación
    df = pd.json_normalize(data)
    if "pacientes.nombre" in df.columns:
        df.rename(columns={"pacientes.nombre": "nombre"}, inplace=True)

    return df


def exportar_turnos_excel(nombre_archivo="turnos.xlsx"):
    df = obtener_turnos()
    df.to_excel(nombre_archivo, index=False)
    return nombre_archivo

