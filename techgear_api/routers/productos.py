from fastapi import APIRouter, HTTPException, Form, File, UploadFile
from bson import ObjectId
from pathlib import Path
import shutil

from techgear_api.models.producto import ProductoRespuesta
from techgear_api.database import productos_collection


router = APIRouter(
    prefix="/productos",
    tags=["Productos"]
)


CARPETA_IMAGENES = Path("techgear_api/imagenes")
CARPETA_IMAGENES.mkdir(parents=True, exist_ok=True)


@router.post("/", response_model=ProductoRespuesta)
async def crear_producto(
    nombre: str = Form(...),
    descripcion: str = Form(...),
    precio: float = Form(...),
    stock: int = Form(...),
    categoria: str = Form(...),
    imagen: UploadFile | None = File(None)
):

    nombre_imagen = ""

    if imagen:
        extension = Path(imagen.filename).suffix
        nombre_imagen = f"{ObjectId()}{extension}"

        ruta_imagen = CARPETA_IMAGENES / nombre_imagen

        with open(ruta_imagen, "wb") as archivo:
            shutil.copyfileobj(imagen.file, archivo)

    datos_producto = {
        "nombre": nombre,
        "descripcion": descripcion,
        "precio": precio,
        "stock": stock,
        "categoria": categoria,
        "imagen": nombre_imagen
    }

    resultado = await productos_collection.insert_one(
        datos_producto
    )

    producto_creado = await productos_collection.find_one(
        {"_id": resultado.inserted_id}
    )

    producto_creado["id"] = str(producto_creado["_id"])
    del producto_creado["_id"]

    return producto_creado


@router.get("/", response_model=list[ProductoRespuesta])
async def obtener_productos():

    productos = await productos_collection.find().to_list(
        length=None
    )

    for producto in productos:
        producto["id"] = str(producto["_id"])
        del producto["_id"]

    return productos


@router.get("/{id}", response_model=ProductoRespuesta)
async def obtener_producto(id: str):

    try:
        producto = await productos_collection.find_one(
            {"_id": ObjectId(id)}
        )
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="ID de producto invalido"
        )

    if producto is None:
        raise HTTPException(
            status_code=404,
            detail="Producto no encontrado"
        )

    producto["id"] = str(producto["_id"])
    del producto["_id"]

    return producto


@router.put("/{id}", response_model=ProductoRespuesta)
async def actualizar_producto(
    id: str,
    nombre: str = Form(...),
    descripcion: str = Form(...),
    precio: float = Form(...),
    stock: int = Form(...),
    categoria: str = Form(...),
    imagen: UploadFile | None = File(None)
):

    try:
        producto_existente = await productos_collection.find_one(
            {"_id": ObjectId(id)}
        )
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="ID de producto invalido"
        )

    if producto_existente is None:
        raise HTTPException(
            status_code=404,
            detail="Producto no encontrado"
        )

    nombre_imagen = producto_existente.get("imagen", "")

    if imagen:
        extension = Path(imagen.filename).suffix
        nombre_imagen = f"{ObjectId()}{extension}"

        ruta_imagen = CARPETA_IMAGENES / nombre_imagen

        with open(ruta_imagen, "wb") as archivo:
            shutil.copyfileobj(imagen.file, archivo)

    datos_actualizados = {
        "nombre": nombre,
        "descripcion": descripcion,
        "precio": precio,
        "stock": stock,
        "categoria": categoria,
        "imagen": nombre_imagen
    }

    await productos_collection.update_one(
        {"_id": ObjectId(id)},
        {"$set": datos_actualizados}
    )

    producto_actualizado = await productos_collection.find_one(
        {"_id": ObjectId(id)}
    )

    producto_actualizado["id"] = str(
        producto_actualizado["_id"]
    )

    del producto_actualizado["_id"]

    return producto_actualizado


@router.delete("/{id}")
async def eliminar_producto(id: str):

    try:
        producto = await productos_collection.find_one(
            {"_id": ObjectId(id)}
        )

        resultado = await productos_collection.delete_one(
            {"_id": ObjectId(id)}
        )

    except Exception:
        raise HTTPException(
            status_code=400,
            detail="ID de producto invalido"
        )

    if resultado.deleted_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Producto no encontrado"
        )

    if producto and producto.get("imagen"):
        ruta_imagen = CARPETA_IMAGENES / producto["imagen"]

        if ruta_imagen.exists():
            ruta_imagen.unlink()

    return {
        "mensaje": "Producto eliminado correctamente",
        "producto_id": id
    }