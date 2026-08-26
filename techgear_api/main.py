from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from techgear_api.routers.productos import router as productos_router
from techgear_api.routers.pedidos import router as pedidos_router


app = FastAPI(
    title="TechGear API"
)


@app.get("/")
def inicio():
    return {
        "mensaje": "Bienvenido a la API de TechGear",
        "documentacion": "Escribe /docs para ver la documentacion de la API"
    }


app.mount(
    "/imagenes",
    StaticFiles(directory="techgear_api/imagenes"),
    name="imagenes"
)


app.include_router(productos_router)
app.include_router(pedidos_router)