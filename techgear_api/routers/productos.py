# ============================================================
# ROUTER DE PRODUCTOS
# ============================================================

from fastapi import APIRouter, HTTPException
from bson import ObjectId

# Modelos de Pydantic
from techgear_api.models.producto import Producto, ProductoRespuesta

# Colección de productos en MongoDB
from techgear_api.database import productos_collection


# Creamos el router
router = APIRouter(
    prefix="/productos",
    tags=["Productos"]
)


# ============================================================
# CREAR PRODUCTO
# POST /productos/
# ============================================================

@router.post("/", response_model=ProductoRespuesta)
async def crear_producto(producto: Producto):

    # Convertimos el modelo Pydantic a diccionario
    datos_producto = producto.model_dump()

    # Guardamos el producto en MongoDB
    resultado = await productos_collection.insert_one(
        datos_producto
    )

    # Buscamos el producto recién creado
    producto_creado = await productos_collection.find_one(
        {"_id": resultado.inserted_id}
    )

    # Convertimos ObjectId a texto
    producto_creado["id"] = str(producto_creado["_id"])

    # Eliminamos el _id de MongoDB
    del producto_creado["_id"]

    return producto_creado


# ============================================================
# OBTENER TODOS LOS PRODUCTOS
# GET /productos/
# ============================================================

@router.get("/", response_model=list[ProductoRespuesta])
async def obtener_productos():

    # Buscamos todos los productos
    productos = await productos_collection.find().to_list(
        length=None
    )

    # Convertimos los ObjectId a texto
    for producto in productos:
        producto["id"] = str(producto["_id"])
        del producto["_id"]

    return productos


# ============================================================
# OBTENER UN PRODUCTO POR ID
# GET /productos/{id}
# ============================================================

@router.get("/{id}", response_model=ProductoRespuesta)
async def obtener_producto(id: str):

    # Validamos que el ID tenga formato válido
    try:
        producto = await productos_collection.find_one(
            {"_id": ObjectId(id)}
        )
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="ID de producto inválido"
        )

    # Si no existe
    if producto is None:
        raise HTTPException(
            status_code=404,
            detail="Producto no encontrado"
        )

    # Convertimos ObjectId a texto
    producto["id"] = str(producto["_id"])

    # Eliminamos _id
    del producto["_id"]

    return producto


# ============================================================
# ACTUALIZAR UN PRODUCTO
# PUT /productos/{id}
# ============================================================

@router.put("/{id}", response_model=ProductoRespuesta)
async def actualizar_producto(
    id: str,
    producto: Producto
):

    # Validamos el ID y buscamos el producto
    try:
        producto_existente = await productos_collection.find_one(
            {"_id": ObjectId(id)}
        )
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="ID de producto inválido"
        )

    # Si no existe
    if producto_existente is None:
        raise HTTPException(
            status_code=404,
            detail="Producto no encontrado"
        )

    # Convertimos los nuevos datos
    datos_actualizados = producto.model_dump()

    # Actualizamos MongoDB
    await productos_collection.update_one(
        {"_id": ObjectId(id)},
        {"$set": datos_actualizados}
    )

    # Buscamos nuevamente el producto
    producto_actualizado = await productos_collection.find_one(
        {"_id": ObjectId(id)}
    )

    # Convertimos ObjectId a texto
    producto_actualizado["id"] = str(
        producto_actualizado["_id"]
    )

    del producto_actualizado["_id"]

    return producto_actualizado


# ============================================================
# ELIMINAR UN PRODUCTO
# DELETE /productos/{id}
# ============================================================

@router.delete("/{id}")
async def eliminar_producto(id: str):

    # Validamos el ID
    try:
        resultado = await productos_collection.delete_one(
            {"_id": ObjectId(id)}
        )
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="ID de producto inválido"
        )

    # Si no existe
    if resultado.deleted_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Producto no encontrado"
        )

    return {
        "mensaje": "Producto eliminado correctamente",
        "producto_id": id
    }