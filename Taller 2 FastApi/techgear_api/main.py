from fastapi import FastAPI
from database import database
from routes import productos, pedidos 

app = FastAPI(
    title="TechGear_API",
    description="API REST para gestionar productos y pedidos de TechGear",
    version="1.0.0"
)

# Incluimos las rutas de productos
app.include_router(productos.router)
# Incluimos las rutas de pedidos
app.include_router(pedidos.router)

@app.get("/")
async def inicio():
    return {
        "mensaje": "Bienvenido a TechGear API",
        "version": "1.0.0"
    }

@app.get("/test-db")
async def test_db():
    try:
        await database.command("ping")
        return {"status": "Conectado exitosamente a MongoDB Atlas 🔥"}
    except Exception as e:
        return {"status": "Error de conexión", "detalle": str(e)}