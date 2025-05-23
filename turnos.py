import pandas as pd
from db import conectar_db


def agendar_turno(paciente_id, fecha, hora, motivo):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO turnos (paciente_id, fecha, hora, motivo)
        VALUES (?, ?, ?, ?)
    """, (paciente_id, fecha, hora, motivo))
    conn.commit()
    conn.close()

def obtener_turnos():
    conn = conectar_db()
    df = pd.read_sql_query("""
        SELECT turnos.id, pacientes.nombre, fecha, hora, motivo
        FROM turnos, pacientes
        WHERE turnos.id = pacientes.id
    """, conn)
    conn.close()
    return df

def exportar_turnos_excel(nombre_archivo="turnos.xlsx"):
    df = obtener_turnos()
    df.to_excel(nombre_archivo, index=False)
    return nombre_archivo

