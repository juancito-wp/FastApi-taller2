from fastapi import APIRouter, HTTPException, status
from bson import ObjectId
from typing import List

from ..database import productos_collection
from ..schemas.producto import ProductoCreate, ProductoUpdate, ProductoResponse

router = APIRouter(
    prefix="/productos",
    tags=["Productos"]
)

def producto_helper(producto) -> dict:
    return {
        "id": str(producto["_id"]),
        "nombre": producto["nombre"],
        "descripcion": producto["descripcion"],
        "precio": producto["precio"],
        "stock": producto["stock"],
        "categoria": producto["categoria"]
    }

# 1. Crear producto
@router.post("/", response_model=ProductoResponse, status_code=status.HTTP_201_CREATED)
async def crear_producto(producto: ProductoCreate):
    nuevo_producto = producto.model_dump()
    resultado = await productos_collection.insert_one(nuevo_producto)
    producto_creado = await productos_collection.find_one({"_id": resultado.inserted_id})
    return producto_helper(producto_creado)

# 2. Listar todos los productos
@router.get("/", response_model=List[ProductoResponse])
async def obtener_productos():
    productos = []
    cursor = productos_collection.find()
    async for producto in cursor:
        productos.append(producto_helper(producto))
    return productos

# 3. Obtener un producto por ID
@router.get("/{id}", response_model=ProductoResponse)
async def obtener_producto(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="ID no válido")
    
    producto = await productos_collection.find_one({"_id": ObjectId(id)})
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    return producto_helper(producto)

# 4. Actualizar producto (PATCH)
@router.patch("/{id}", response_model=ProductoResponse)
async def actualizar_producto(id: str, producto_update: ProductoUpdate):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="ID no válido")
    
    # Excluimos los campos no enviados (None)
    datos_actualizar = {k: v for k, v in producto_update.model_dump().items() if v is not None}
    
    if not datos_actualizar:
        raise HTTPException(status_code=400, detail="No se enviaron campos para actualizar")
    
    resultado = await productos_collection.update_one(
        {"_id": ObjectId(id)},
        {"$set": datos_actualizar}
    )
    
    if resultado.matched_count == 0:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
        
    producto_actualizado = await productos_collection.find_one({"_id": ObjectId(id)})
    return producto_helper(producto_actualizado)

# 5. Eliminar producto
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_producto(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="ID no válido")
    
    resultado = await productos_collection.delete_one({"_id": ObjectId(id)})
    if resultado.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    return None