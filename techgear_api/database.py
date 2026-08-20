import os
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

# CARGAR VARIABLES DE ENTORNO
load_dotenv()


# OBTENER LA URL DE MONGODB ATLAS
MONGODB_URL = os.getenv("MONGODB_URL")


# INICIALIZAR EL CLIENTE DE MONGODB
client = AsyncIOMotorClient(MONGODB_URL)


# SELECCIONAR LA BASE DE DATOS DE TECHGEAR
database = client.TechGear


# SELECCIONAR LAS COLECCIONES DE TECHGEAR
productos_collection = database.productos
pedidos_collection = database.pedidos


# FUNCIÓN PARA PROBAR LA CONEXIÓN
async def test_connection():

    try:

        await client.admin.command("ping")

        print("Conexión a MongoDB Atlas exitosa")
        print("Base de datos seleccionada: TechGear")

    except Exception as e:

        print(f"Error al conectar a MongoDB: {e}")


# EJECUTAR LA PRUEBA
if __name__ == "__main__":
    asyncio.run(test_connection())