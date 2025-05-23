import sqlite3


def conectar_db():
    conn = sqlite3.connect("data/turnos.db", check_same_thread=False)
    return conn


def crear_tablas():
    conn = conectar_db()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pacientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        telefono TEXT,
        observaciones TEXT
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS turnos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        paciente_id INTEGER,
        fecha TEXT,
        hora TEXT,
        motivo TEXT,
        FOREIGN KEY(paciente_id) REFERENCES pacientes(id)
    );
    """)

    conn.commit()
    conn.close()
