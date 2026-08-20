from fastapi import FastAPI

from routers.productos import router as productos_router
from routers.pedidos import router as pedidos_router


app = FastAPI(
    title="TechGear API"
)


app.include_router(productos_router)
app.include_router(pedidos_router)