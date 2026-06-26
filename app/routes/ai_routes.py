from fastapi import APIRouter, HTTPException
from app.database.database import SessionLocal
from app.models.inventario import Inventario
from app.models.producto import Producto
from app.services.ia_service import sugerir_recetas
router = APIRouter(
prefix="/ia",
tags=["IA"]
)

@router.get("/sugerir/{usuario_id}")
def sugerir(usuario_id : int):
    db = SessionLocal()
    try:
        items = db.query(Inventario, Producto).join(
            Producto, Inventario.producto_id == Producto.id_producto
        ).filter(
            Inventario.usuario_id == usuario_id
        ).all()
        if not items:
            raise HTTPException(
                status_code=404,
                detail="El usuario no tiene producto en el inventario"
            )
        productos =[
            {"nombre": producto.nombre, "cantidad":inventario.cantidad, "id_producto":producto.id_producto}
            for inventario, producto in items
        ]
        respuesta = sugerir_recetas(productos)
        return{"sugerencias": respuesta}
    except HTTPException:
        raise
    except Exception as e: 
        raise HTTPException(
            status_code=500, 
            detail=str(e)
        )
    finally:
        db.close()