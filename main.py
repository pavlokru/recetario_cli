"""Servidor Web FastAPI: Punto de entrada (Refactorizado sin advertencias)."""

import os
import shutil
import uuid
from typing import Annotated

from fastapi import FastAPI, File, Form, Request, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from core import CatalogEngine
from data import RECETARIO_BASE

app = FastAPI(title="Recetario Web API")

# Aseguramos que el directorio de subidas exista
UPLOAD_DIR = "static/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

engine = CatalogEngine(archivo_json="recetario.json", datos_iniciales=RECETARIO_BASE)


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    """Ruta principal web (síncrona)."""
    recetas = engine.obtener_todos()
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"recetas": recetas},
    )


@app.get("/buscar", response_class=HTMLResponse)
def buscar(request: Request, q: str = ""):
    recetas = engine.buscar(q)
    return templates.TemplateResponse(
        request=request,
        name="partials/lista_recetas.html",
        context={"recetas": recetas},
    )


@app.get("/receta/{receta_id}", response_class=HTMLResponse)
def detalle(request: Request, receta_id: int):
    receta = engine.obtener_por_id(receta_id)
    return templates.TemplateResponse(
        request=request,
        name="partials/detalle_receta.html",
        context={"receta": receta},
    )


@app.post("/receta/{receta_id}/nota", response_class=HTMLResponse)
def agregar_nota(
    request: Request,
    receta_id: int,
    # Solución 1: Usar Annotated para evitar B008
    nueva_nota: Annotated[str, Form()],
):
    engine.agregar_nota(receta_id, nueva_nota)
    receta = engine.obtener_por_id(receta_id)
    return templates.TemplateResponse(
        request=request,
        name="partials/detalle_receta.html",
        context={"receta": receta},
    )


@app.get("/formulario_receta", response_class=HTMLResponse)
def formulario_receta(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="partials/formulario_receta.html",
        context={},
    )


@app.post("/receta", response_class=HTMLResponse)
# Solución 2: Usar 'def' en vez de 'async def' permite usar open() sin advertencias
def crear_receta(
    request: Request,
    nombre: Annotated[str, Form()],
    ingredientes_raw: Annotated[str, Form()],
    pasos_raw: Annotated[str, Form()],
    categoria: Annotated[str, Form()] = "",
    origen: Annotated[str, Form()] = "",
    dificultad: Annotated[str, Form()] = "Fácil",
    tiempo_preparacion_min: Annotated[int | None, Form()] = None,
    etiquetas_raw: Annotated[str, Form()] = "",
    # La foto ahora usa Annotated y asume None como valor por defecto estándar
    foto: Annotated[UploadFile | None, File()] = None,
):
    """Procesa el formulario, guarda la imagen y crea la receta de forma síncrona."""

    ingredientes = [i.strip() for i in ingredientes_raw.split(",") if i.strip()]
    pasos = [p.strip() for p in pasos_raw.split(".") if p.strip()]
    etiquetas = [e.strip() for e in etiquetas_raw.split(",") if e.strip()]

    imagen_url = None
    if foto and foto.filename:
        ext = os.path.splitext(foto.filename)[1]
        nombre_archivo = f"{uuid.uuid4().hex}{ext}"
        ruta_archivo = os.path.join(UPLOAD_DIR, nombre_archivo)

        # Al usar 'def' en la función principal, este open() ya no genera conflicto
        with open(ruta_archivo, "wb") as buffer:
            shutil.copyfileobj(foto.file, buffer)

        imagen_url = f"/static/uploads/{nombre_archivo}"

    engine.agregar_item(
        nombre=nombre,
        categoria=categoria,
        origen=origen,
        dificultad=dificultad,
        tiempo_preparacion_min=tiempo_preparacion_min,
        porciones=None,
        ingredientes=ingredientes,
        pasos=pasos,
        etiquetas=etiquetas,
        imagen_url=imagen_url,
    )

    recetas = engine.obtener_todos()
    return templates.TemplateResponse(
        request=request,
        name="partials/lista_recetas.html",
        context={"recetas": recetas},
    )
