from fastapi import FastAPI
from app.api.v1 import contract_routes

app = FastAPI(
    title="Generador de Contratos Automatizados",
    description="API para crear contratos digitales de manera eficiente y profesional.",
    version="0.1.0"
)

# Incluir las rutas de contratos
app.include_router(contract_routes.router, prefix="/api/v1/contracts", tags=["Contratos"])

@app.get("/")
def read_root():
    return {"message": "Bienvenido a la API de Generación de Contratos"}