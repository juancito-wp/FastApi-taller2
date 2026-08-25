from fastapi import APIRouter, HTTPException, status
from bson import ObjectId

from database import pedidos_collection, productos_collection
from schemas.pedido import PedidoCreate

router = APIRouter(prefix="/pedidos", tags=["Pedidos"])

@router.post("/", status_code=status.HTTP_201_CREATED)
async def crear_pedido(pedido: PedidoCreate):
    # 1. Validar productos y stock disponible
    for item in pedido.productos:
        prod_id_str = str(item.producto_id)
        cantidad_num = int(item.cantidad)

        # Buscar por ObjectId o String
        try:
            query = {"_id": ObjectId(prod_id_str)}
        except Exception:
            query = {"_id": prod_id_str}

        producto = await productos_collection.find_one(query)
        if not producto:
            producto = await productos_collection.find_one({"_id": prod_id_str})

        if not producto:
            raise HTTPException(
                status_code=404, 
                detail=f"El producto con ID {prod_id_str} no existe."
            )
        
        if producto.get("stock", 0) < cantidad_num:
            raise HTTPException(
                status_code=400, 
                detail=f"Stock insuficiente para '{producto.get('nombre')}'. Disponible: {producto.get('stock')}"
            )

    # 2. Descontar el stock en MongoDB Atlas
    for item in pedido.productos:
        prod_id_str = str(item.producto_id)
        cantidad_num = int(item.cantidad)

        try:
            query = {"_id": ObjectId(prod_id_str)}
        except Exception:
            query = {"_id": prod_id_str}

        res = await productos_collection.update_one(
            query,
            {"$inc": {"stock": -cantidad_num}}
        )

        if res.matched_count == 0:
            await productos_collection.update_one(
                {"_id": prod_id_str},
                {"$inc": {"stock": -cantidad_num}}
            )

    # 3. Guardar la orden en MongoDB
    nuevo_pedido = pedido.dict()
    resultado = await pedidos_collection.insert_one(nuevo_pedido)

    return {
        "mensaje": "Pedido realizado con éxito",
        "pedido_id": str(resultado.inserted_id)
    }