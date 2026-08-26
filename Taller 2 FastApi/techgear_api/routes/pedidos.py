from fastapi import APIRouter, HTTPException, status
from bson import ObjectId

from ..database import pedidos_collection, productos_collection
from ..schemas.pedido import PedidoCreate, PedidoResponse, PedidoResumen

router = APIRouter(prefix="/pedidos", tags=["Pedidos"])


@router.get("/resumen", response_model=list[PedidoResumen])
async def obtener_resumen_pedidos():
    resumen = pedidos_collection.aggregate([
        {
            "$group": {
                "_id": {"usuario": "$usuario", "correo": "$correo"},
                "cantidad_pedidos": {"$sum": 1},
                "total_compras": {"$sum": {"$ifNull": ["$total", 0]}},
            }
        },
        {"$sort": {"total_compras": -1}},
        {
            "$project": {
                "_id": 0,
                "usuario": "$_id.usuario",
                "correo": "$_id.correo",
                "cantidad_pedidos": 1,
                "total_compras": 1,
            }
        },
    ])
    return [registro async for registro in resumen]

@router.post("/", response_model=PedidoResponse, status_code=status.HTTP_201_CREATED)
async def crear_pedido(pedido: PedidoCreate):
    # 1. Validar productos y stock disponible
    productos_pedido = []
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

        productos_pedido.append({
            "producto_id": prod_id_str,
            "nombre": producto["nombre"],
            "cantidad": cantidad_num,
            "precio_unitario": producto["precio"],
        })

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
    total = sum(item["cantidad"] * item["precio_unitario"] for item in productos_pedido)
    nuevo_pedido = {
        "usuario": pedido.usuario,
        "correo": str(pedido.correo),
        "productos": productos_pedido,
        "total": total,
    }
    resultado = await pedidos_collection.insert_one(nuevo_pedido)

    return {
        "id": str(resultado.inserted_id),
        "usuario": pedido.usuario,
        "correo": pedido.correo,
        "productos": productos_pedido,
        "total": total,
    }