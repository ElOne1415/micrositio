# Importación de dependencias principales
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
import sqlite3, json
from backend.database import get_connection  # función que abre la conexión a la BD

# Definimos un router para organizar las rutas relacionadas con "estudiante"
router = APIRouter()


# -------------------------------
# 📌 Ruta para crear la base de datos y tablas
# -------------------------------
@router.get("/create-db/")
def create_db():
    conn = get_connection()      # Conexión a la base de datos
    cursor = conn.cursor()

    # Tabla de estudiantes: contiene información principal del perfil
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS estudiante (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            foto TEXT,
            perfil TEXT NOT NULL,
            contacto TEXT NOT NULL
        )
    ''')

    # Tabla de proyectos: vinculada a cada estudiante (relación 1:N)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS proyectos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            estudiante_id INTEGER,
            nombre TEXT NOT NULL,
            descripcion TEXT NOT NULL,
            FOREIGN KEY (estudiante_id) REFERENCES estudiante(id)
        )
    ''')

    # Tabla de skills/habilidades: vinculada a cada estudiante (relación 1:N)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS skills (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            estudiante_id INTEGER,
            nombre TEXT NOT NULL,
            FOREIGN KEY (estudiante_id) REFERENCES estudiante(id)
        )
    ''')

    conn.commit()   # Guardamos cambios
    conn.close()    # Cerramos conexión

    # Respondemos en formato JSON con un código HTTP 201 (Created)
    return JSONResponse(
        content={"message": "Tablas de estudiante creadas correctamente"},
        status_code=status.HTTP_201_CREATED
    )


# -------------------------------
# 📌 Ruta para insertar datos iniciales (semilla de prueba)
# -------------------------------
@router.get("/init-data/")
def init_data():
    conn = get_connection()
    cursor = conn.cursor()

    # Limpieza previa: borramos datos existentes para evitar duplicados
    cursor.execute("DELETE FROM estudiante")
    cursor.execute("DELETE FROM proyectos")
    cursor.execute("DELETE FROM skills")

    # Insertamos el estudiante principal
    cursor.execute('''
        INSERT INTO estudiante (nombre, foto, perfil, contacto)
        VALUES (?, ?, ?, ?)
    ''', (
        "Juan Diego Fajardo Suárez",
        "https://media.licdn.com/dms/image/v2/D4E03AQEYjAG-aFnVpw/profile-displayphoto-shrink_800_800/profile-displayphoto-shrink_800_800/0/1712167191210?e=1761177600&v=beta&t=DTQyxHEckCG2fhWvRQLfw2XbZ_Ec0LCXizQspouAyTU",
        "Soy estudiante de Ingeniería de Software en la Universidad Manuela Beltrán y Técnico en Programación de Software (SENA). Actualmente me desempeño como practicante en Crona Grival, donde apoyo el desarrollo de soluciones backend e integración de sistemas. Me apasiona el diseño de arquitecturas eficientes, la optimización de procesos y la creación de herramientas que generen impacto real en entornos productivos.",
        json.dumps({   # Guardamos el contacto como JSON serializado en un campo TEXT
            "email": "fajardojuan735@gmail.com",
            "linkedin": "https://www.linkedin.com/in/juan-fajardo-27b57726b"
        })
    ))

    # Obtenemos el ID autogenerado del estudiante para relacionar sus proyectos y skills
    estudiante_id = cursor.lastrowid

    # Insertamos proyectos asociados
    proyectos = [
        ("Sistema de Control de Inventarios", "Aplicación CRUD para la gestión de productos y reportes, optimizando tiempos de consulta y reduciendo errores de registro."),
        ("Aplicación de Requerimientos – Crona Grival", "Plataforma interna que centraliza solicitudes de distintas áreas, mejorando la trazabilidad y el flujo de trabajo."),
        ("App de Reporte de Rotura – Crona Grival", "Aplicación en tiempo real que permite registrar defectos en producción, contribuyendo a la mejora continua."),
        ("Plataforma de Gestión de Tareas", "Aplicación personal desarrollada con FastAPI y SQLite para organización y priorización de actividades.")
    ]
    cursor.executemany(
        "INSERT INTO proyectos (estudiante_id, nombre, descripcion) VALUES (?, ?, ?)",
        [(estudiante_id, p[0], p[1]) for p in proyectos]
    )

    # Insertamos las habilidades (skills)
    skills = ["Python", "JavaScript", "FastAPI", "React", "SQL", "Git/GitHub", "Docker"]
    cursor.executemany(
        "INSERT INTO skills (estudiante_id, nombre) VALUES (?, ?)",
        [(estudiante_id, s) for s in skills]
    )

    conn.commit()
    conn.close()
    return {"message": "Datos iniciales de estudiante insertados correctamente"}


# -------------------------------
# 📌 Ruta para obtener el perfil del estudiante con proyectos y skills
# -------------------------------
@router.get("/estudiante")
def get_estudiante():
    conn = get_connection()
    cursor = conn.cursor()

    # Consultamos el estudiante (solo el primero registrado)
    cursor.execute("SELECT id, nombre, foto, perfil, contacto FROM estudiante LIMIT 1")
    row = cursor.fetchone()
    if not row:
        return {"error": "No hay estudiante registrado"}

    # Desestructuramos los campos de la consulta
    estudiante_id, nombre, foto, perfil, contacto_str = row
    contacto = json.loads(contacto_str)  # convertimos el contacto a dict (antes estaba en JSON string)

    # Traemos proyectos relacionados
    cursor.execute("SELECT nombre, descripcion FROM proyectos WHERE estudiante_id=?", (estudiante_id,))
    proyectos = [{"nombre": r[0], "descripcion": r[1]} for r in cursor.fetchall()]

    # Traemos skills relacionados
    cursor.execute("SELECT nombre FROM skills WHERE estudiante_id=?", (estudiante_id,))
    skills = [r[0] for r in cursor.fetchall()]

    conn.close()

    # Retornamos toda la info en un JSON bien estructurado
    return {
        "nombre": nombre,
        "foto": foto,
        "perfil": perfil,
        "contacto": contacto,
        "proyectos": proyectos,
        "skills": skills
    }
