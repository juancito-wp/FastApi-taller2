import os
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

# Lee la variable del archivo .env
MONGODB_URL = os.getenv("MONGODB_URL")

# Inicializa el cliente de MongoDB Atlas
client = AsyncIOMotorClient(MONGODB_URL)

# Selecciona la base de datos de TechGear (puedes nombrarla techgear_db)
database = client.techgear_db

# Selecciona las colecciones requeridas para la API
productos_collection = database.productos
pedidos_collection = database.pedidos