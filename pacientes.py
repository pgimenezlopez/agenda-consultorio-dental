from supabase_config import supabase
import pandas as pd

def agregar_paciente(nombre, telefono, observaciones):
    supabase.table("pacientes").insert({
        "nombre": nombre,
        "telefono": telefono,
        "observaciones": observaciones
    }).execute()

def obtener_pacientes():
    response = supabase.table("pacientes").select("*").execute()
    data = response.data if response.data else []
    return pd.DataFrame(data)



def exportar_pacientes_excel(nombre_archivo="pacientes.xlsx"):
    df = obtener_pacientes()
    df.to_excel(nombre_archivo, index=False)
    return nombre_archivo
