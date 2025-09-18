from fastapi import APIRouter
from pydantic import BaseModel, EmailStr
from backend.database import get_connection

router = APIRouter()

class Contacto(BaseModel):
    nombre: str
    email: EmailStr
    mensaje: str

# Endpoint para guardar mensaje en BD
@router.post("/contacto")
def enviar_contacto(contacto: Contacto):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO contacto (nombre, email, mensaje)
        VALUES (?, ?, ?)
    """, (contacto.nombre, contacto.email, contacto.mensaje))

    conn.commit()
    conn.close()

    return {"status": "ok", "mensaje": "Mensaje guardado en la base de datos"}

# Endpoint para listar todos los mensajes
@router.get("/contacto")
def listar_contactos():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM contacto")
    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]
