#Define el endpoint para recibir los datos, guardar archivo adjunto y devolver el contrato generado.

from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse
from app.services.contract_service import render_contract
import shutil
import os

router = APIRouter()

@router.post("/generate", response_class=FileResponse, summary="Genera un contrato de prestación de servicios")
async def generate_contract(
    # Campos del formulario (uno por cada dato relevante)
    nombre_contratante: str = Form(...),
    rut_contratante: str = Form(...),
    email_contratante: str = Form(...),
    direccion_contratante: str = Form(...),

    nombre_contratista: str = Form(...),
    rut_contratista: str = Form(...),
    email_contratista: str = Form(...),
    direccion_contratista: str = Form(...),

    fecha_inicio: str = Form(...),
    servicios: str = Form(...),
    honorarios: str = Form(...),
    plazo: str = Form(...),
    condiciones: str = Form(""),

    documento: UploadFile = File(None)   # Archivo adjunto opcional
):
    """
    Endpoint que recibe datos del contrato, genera el documento y lo devuelve al usuario.
    Puede recibir un archivo adjunto (cédula, anexo) para almacenar o procesar posteriormente.
    """
    # Si se subió un documento, lo guardamos en la carpeta docs_adjuntos/
    if documento:
        doc_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'templates', 'docs_adjuntos')
        os.makedirs(doc_dir, exist_ok=True)
        doc_path = os.path.join(doc_dir, documento.filename)
        with open(doc_path, "wb") as buffer:
            shutil.copyfileobj(documento.file, buffer)
        # Aquí podrías procesar el documento con OCR, por ahora solo se almacena

    # Preparamos el diccionario de datos para el contrato
    contract_context = {
        "nombre_contratante": nombre_contratante,
        "rut_contratante": rut_contratante,
        "email_contratante": email_contratante,
        "direccion_contratante": direccion_contratante,
        "nombre_contratista": nombre_contratista,
        "rut_contratista": rut_contratista,
        "email_contratista": email_contratista,
        "direccion_contratista": direccion_contratista,
        "fecha_inicio": fecha_inicio,
        "servicios": servicios,
        "honorarios": honorarios,
        "plazo": plazo,
        "condiciones": condiciones
    }

    # Generamos el contrato usando el servicio
    try:
        output_path = render_contract(contract_context)
        # Devolvemos el archivo generado como descarga directa
        return FileResponse(
            output_path,
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            filename=os.path.basename(output_path)
        )
    except Exception as e:
        # En caso de error, enviamos un mensaje y código de error HTTP 500
        raise HTTPException(status_code=500, detail=f"No se pudo generar el contrato: {e}")
