import os
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Obtener la URL de conexión desde las variables de entorno
MONGODB_URL = os.getenv("MONGODB_URL")

# Inicializar el cliente de MongoDB
client = AsyncIOMotorClient(MONGODB_URL)

# Seleccionar la base de datos
database = client.ambiente502

# Seleccionar la colección
collection = database.mesas


# Función para probar la conexión a la base de datos
async def test_connection():
    try:
        # Verificar la conexión al servidor MongoDB
        await client.admin.command("ping")
        print("Conexión a MongoDB exitosa")

        # Crear un documento de prueba
        doctest = {
            "nombre": "Rudy Palacios Ayala",
            "edad": 42,
            "genero": "Femenino"
        }

        # Guardar el documento en la colección
        print("Guardando documento en la colección...")
        result = await collection.insert_one(doctest)

        print(f"Documento guardado con ID: {result.inserted_id}")

        # Buscar el documento guardado
        datarequest = await collection.find_one(
            {"_id": result.inserted_id}
        )

        print(f"Documento encontrado: {datarequest}")

    except Exception as e:
        print(f"Error al conectar a MongoDB: {e}")


# Ejecutar la prueba de conexión
if __name__ == "__main__":
    asyncio.run(test_connection())