import pandas as pd
from db import conectar_db

def agregar_paciente(nombre, telefono, observaciones):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO pacientes (nombre, telefono, observaciones) VALUES (?, ?, ?)",
                   (nombre, telefono, observaciones))
    conn.commit()
    conn.close()

def obtener_pacientes():
    conn = conectar_db()
    df = pd.read_sql_query("SELECT * FROM pacientes", conn)
    conn.close()
    return df

def exportar_pacientes_excel(nombre_archivo="pacientes.xlsx"):
    df = obtener_pacientes()
    df.to_excel(nombre_archivo, index=False)
    return nombre_archivo
