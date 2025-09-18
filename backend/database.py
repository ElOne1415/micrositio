import sqlite3

DB_NAME = "micrositio.db"

def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

# Crear tablas si no existen
def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # Tabla para mensajes de contacto
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS contacto (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            email TEXT NOT NULL,
            mensaje TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()

# Llamamos a init_db() cuando se importe
init_db()
