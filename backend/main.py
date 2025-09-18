from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

# Routers
from backend.routers import estudiante, jugadores, contacto
app = FastAPI()

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(estudiante.router)
app.include_router(jugadores.router)
app.include_router(contacto.router)

# Montar frontend
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")
