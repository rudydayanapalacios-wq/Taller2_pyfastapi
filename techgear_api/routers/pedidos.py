# ============================================================
# ROUTER DE PEDIDOS
# ============================================================

from fastapi import APIRouter, HTTPException
from bson import ObjectId

from models.pedido import Pedido
from database import pedidos_collection, productos_collection


# Creamos el router para los endpoints de pedidos
router = APIRouter(
    prefix="/pedidos",
    tags=["Pedidos"]
)


# ============================================================
# CREAR UN PEDIDO
# POST /pedidos/
# ============================================================

@router.post("/")
async def crear_pedido(pedido: Pedido):

    # --------------------------------------------------------
    # Verificamos que el producto exista
    # --------------------------------------------------------

    producto = await productos_collection.find_one(
        {"_id": ObjectId(pedido.producto_id)}
    )

    if producto is None:
        raise HTTPException(
            status_code=404,
            detail="Producto no encontrado"
        )

    # --------------------------------------------------------
    # Verificamos que haya suficiente stock
    # --------------------------------------------------------

    if producto["stock"] < pedido.cantidad:
        raise HTTPException(
            status_code=400,
            detail="Stock insuficiente"
        )

    # --------------------------------------------------------
    # Convertimos el pedido de Pydantic a diccionario
    # --------------------------------------------------------

    datos_pedido = pedido.model_dump()

    # --------------------------------------------------------
    # Guardamos el pedido en MongoDB
    # --------------------------------------------------------

    resultado = await pedidos_collection.insert_one(
        datos_pedido
    )

    # --------------------------------------------------------
    # Actualizamos el stock del producto
    # --------------------------------------------------------

    await productos_collection.update_one(
        {"_id": ObjectId(pedido.producto_id)},
        {
            "$inc": {
                "stock": -pedido.cantidad
            }
        }
    )

    # --------------------------------------------------------
    # Devolvemos la confirmación
    # --------------------------------------------------------

    return {
        "mensaje": "Pedido creado correctamente",
        "pedido_id": str(resultado.inserted_id),
        "cliente": pedido.cliente,
        "producto_id": pedido.producto_id,
        "cantidad": pedido.cantidad,
        "total": pedido.total
    }

# ============================================================
# OBTENER TODOS LOS PEDIDOS
# GET /pedidos/
# ============================================================

@router.get("/")
async def obtener_pedidos():

    pedidos = []

    # Buscamos todos los pedidos en MongoDB
    cursor = pedidos_collection.find()

    async for pedido in cursor:

        # Convertimos ObjectId a texto
        pedido["id"] = str(pedido["_id"])
        del pedido["_id"]

        pedidos.append(pedido)

    return pedidos

# ============================================================
# OBTENER UN PEDIDO POR ID
# GET /pedidos/{id}
# ============================================================

@router.get("/{id}")
async def obtener_pedido(id: str):

    # Convertimos el ID recibido en ObjectId de MongoDB
    try:
        pedido = await pedidos_collection.find_one(
            {"_id": ObjectId(id)}
        )
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="ID de pedido inválido"
        )

    # Si no encontramos el pedido
    if pedido is None:
        raise HTTPException(
            status_code=404,
            detail="Pedido no encontrado"
        )

    # Convertimos ObjectId a texto
    pedido["id"] = str(pedido["_id"])
    del pedido["_id"]

    return pedido

# ============================================================
# ELIMINAR UN PEDIDO
# DELETE /pedidos/{id}
# ============================================================

@router.delete("/{id}")
async def eliminar_pedido(id: str):

    # Convertimos el ID recibido en ObjectId
    try:
        resultado = await pedidos_collection.delete_one(
            {"_id": ObjectId(id)}
        )
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="ID de pedido inválido"
        )

    # Si no se eliminó ningún documento
    if resultado.deleted_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Pedido no encontrado"
        )

    return {
        "mensaje": "Pedido eliminado correctamente",
        "pedido_id": id
    }

# ============================================================
# ACTUALIZAR UN PEDIDO
# PUT /pedidos/{id}
# ============================================================

@router.put("/{id}")
async def actualizar_pedido(id: str, pedido: Pedido):

    # Buscamos el pedido por su ID
    try:
        pedido_existente = await pedidos_collection.find_one(
            {"_id": ObjectId(id)}
        )
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="ID de pedido inválido"
        )

    # Si no existe
    if pedido_existente is None:
        raise HTTPException(
            status_code=404,
            detail="Pedido no encontrado"
        )

    # Actualizamos los datos del pedido
    datos_actualizados = pedido.model_dump()

    await pedidos_collection.update_one(
        {"_id": ObjectId(id)},
        {
            "$set": datos_actualizados
        }
    )

    return {
        "mensaje": "Pedido actualizado correctamente",
        "pedido_id": id,
        "cliente": pedido.cliente,
        "producto_id": pedido.producto_id,
        "cantidad": pedido.cantidad,
        "total": pedido.total
    }