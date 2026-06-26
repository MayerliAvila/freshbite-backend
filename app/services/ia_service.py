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
def sugerir(usuario_id: int):
    """
    Sugiere recetas basadas en los productos del inventario del usuario.

    - **usuario_id**: ID del usuario cuyo inventario se consultará.
    - Retorna una lista de sugerencias generadas por el servicio de IA.
    - Lanza 404 si el usuario no tiene productos en su inventario.
    - Lanza 500 ante cualquier error inesperado del servidor.
    """

    db = SessionLocal()

    try:
        # Consulta el inventario del usuario haciendo JOIN con la tabla de productos
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

        # Construye la lista de productos con los datos necesarios para la IA
        productos = [
            {
                "nombre":      producto.nombre,
                "cantidad":    inventario.cantidad,
                "id_producto": producto.id_producto
            }
            for inventario, producto in items
        ]

        # Envía los productos al servicio de IA y obtiene las sugerencias
        respuesta = sugerir_recetas(productos)

        return {"sugerencias": respuesta}

    except HTTPException:
        raise  # Re-lanza errores HTTP controlados sin modificarlos

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

    finally:
        db.close()  # Cierra la sesión de BD en cualquier escenario