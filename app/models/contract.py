#Define el modelo de datos que el endpoint recibirá y usará.

from pydantic import BaseModel, Field, EmailStr
from typing import Optional

class ContractData(BaseModel):
    # Datos de la parte contratante (quien contrata el servicio)
    nombre_contratante: str = Field(..., example="Juan Pérez")
    rut_contratante: str = Field(..., example="12.345.678-9")
    email_contratante: EmailStr
    direccion_contratante: str

    # Datos de la parte contratista (quien presta el servicio)
    nombre_contratista: str = Field(..., example="Empresa Servicios SPA")
    rut_contratista: str
    email_contratista: EmailStr
    direccion_contratista: str

    # Detalles del contrato
    fecha_inicio: str = Field(..., example="2024-07-24")   # Formato YYYY-MM-DD
    servicios: str = Field(..., example="Desarrollo de plataforma web") # Descripción
    honorarios: str = Field(..., example="$1.000.000")     # Valor pactado
    plazo: str = Field(..., example="3 meses")
    condiciones: Optional[str] = Field(None, example="Condiciones adicionales si aplica")  # Opcional
