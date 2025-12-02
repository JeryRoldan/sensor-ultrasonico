from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from pydantic import BaseModel

app = FastAPI()

# Habilitar CORS para ESP32 y Web
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Archivos estáticos (CSS + JS)
app.mount("/static", StaticFiles(directory="templates"), name="static")

# Cargar HTML
templates = Jinja2Templates(directory="templates")

# Lista temporal para guardar registros
distancias = []

# Modelo recibido desde ESP32
class Distancia(BaseModel):
    distancia: float

# Página web
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# ESP32 envía datos
@app.post("/api/distancia")
async def recibir_distancia(data: Distancia):
    registro = {
        "fecha": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "distancia": data.distancia
    }
    distancias.append(registro)
    print("Distancia recibida:", data.distancia)
    return {"status": "ok"}

# Web obtiene datos
@app.get("/api/distancia")
async def obtener_datos():
    return distancias[-20:]  # Últimos 20 registros
