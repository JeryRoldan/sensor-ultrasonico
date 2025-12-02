from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Modelo de datos
class Distancia(BaseModel):
    distancia: float

@app.get("/")
def home():
    return {"msg": "API funcionando en Render"}

@app.post("/api/distancia")
def recibir_distancia(data: Distancia):
    print(f"Distancia recibida: {data.distancia} cm")
    return {"status": "ok", "distancia": data.distancia}
