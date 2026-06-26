from datetime import datetime

from fastapi import APIRouter, HTTPException, status
from sqlalchemy import func
from app.database.database import SessionLocal
from app.models.categoria import Categoria
from app.models.estado import Estado
from app.models.inventario import Inventario
from app.models.producto import Producto
from app.schemas.inventario_schema import *
from app.services.inventario_service import actualizar_estados

router = APIRouter(
    prefix="/inventarios",
    tags=["Inventarios"]
)

# ── AGREGAR AL INVENTARIO ────────────────────────────────────────────────
@router.post("/", status_code=status.HTTP_201_CREATED, summary="Agregar producto al inventario")
def crearInventario(inventario: InventarioCreate):
    """Registra un nuevo producto en el inventario de un usuario con cantidad, fechas y estado."""
    db = SessionLocal()
    try:
        nuevo_inventario = Inventario(
            usuario_id=inventario.usuario_id,
            producto_id=inventario.producto_id,
            cantidad=inventario.cantidad,
            fecha_ingreso=datetime.now(),
            fecha_vencimiento=inventario.fecha_vencimiento,
            estado_id=inventario.estado_id
        )
        db.add(nuevo_inventario)
        db.commit()
        db.refresh(nuevo_inventario)

        return {
            "mensaje": "Inventario creado correctamente",
            "data": nuevo_inventario
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error al crear inventario: {str(e)}"
        )
    finally:
        db.close()


# ── INVENTARIO DE UN USUARIO ──────────────────────────────────────────────
@router.get("/usuario/{id_usuario}", summary="Ver inventario de un usuario")
def obtenerInventarioPorUsuario(id_usuario: int):
    """
    Retorna todos los productos del inventario pertenecientes a un usuario específico.
    """

    db = SessionLocal()

    try:

        inventarios = (
            db.query(
                Inventario.id_inventario,
                Producto.nombre.label("nombre_producto"),
                Inventario.cantidad,
                Estado.nombre.label("nombre_estado"),
                Inventario.fecha_vencimiento
            )
            .join(
                Producto,
                Inventario.producto_id == Producto.id_producto
            )
            .join(
                Estado,
                Inventario.estado_id == Estado.id_estado
            )
            .filter(
                Inventario.usuario_id == id_usuario
            )
            .all()
        )

        resultado = []

        for item in inventarios:
            resultado.append({
                "id_inventario": item.id_inventario,
                "nombre_producto": item.nombre_producto,
                "cantidad": item.cantidad,
                "estado": item.nombre_estado,
                "fecha_vencimiento": item.fecha_vencimiento
            })

        return resultado

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al obtener inventario del usuario: {str(e)}"
        )

    finally:
        db.close()


@router.get("/despensa/{id_usuario}", summary="Ver inventario de un usuario")
def obtenerInventarioPorUsuario(id_usuario: int):
    """
    Retorna todos los productos del inventario pertenecientes a un usuario específico.
    """

    db = SessionLocal()

    try:

        inventarios = (
            db.query(
                Inventario.id_inventario,
                Producto.nombre.label("nombre_producto"),
                Categoria.nombre.label("nombre_categoria"),
                Inventario.cantidad,
                Estado.nombre.label("nombre_estado"),
                Inventario.fecha_vencimiento
            )
            .join(
                Producto,
                Inventario.producto_id == Producto.id_producto
            )
            .join(
                Categoria,
                Categoria.id_categoria == Producto.categoria_id
            )
            .join(
                Estado,
                Inventario.estado_id == Estado.id_estado
            )
            .filter(
                Inventario.usuario_id == id_usuario
            )
            .all()
        )

        resultado = []

        for item in inventarios:
            resultado.append({
                "id_inventario": item.id_inventario,
                "nombre_producto": item.nombre_producto,
                "categoria":item.nombre_categoria,
                "cantidad": item.cantidad,
                "estado": item.nombre_estado,
                "fecha_vencimiento": item.fecha_vencimiento
            })

        return resultado

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al obtener inventario del usuario: {str(e)}"
        )

    finally:
        db.close()

# ── ACTUALIZAR INVENTARIO ──────────────────────────────────────────────────
@router.put("/{id_inventario}", summary="Actualizar ítem del inventario")
def actualizarInventario(id_inventario: int, inventario: InventarioEditar):
    """Actualiza la cantidad, fecha de vencimiento o estado de un ítem del inventario."""
    db = SessionLocal()
    try:
        actualizar = db.query(Inventario).filter(
            Inventario.id_inventario == id_inventario
        ).first()

        if not actualizar:
            raise HTTPException(
                status_code=404,
                detail="Inventario no encontrado"
            )

        actualizar.cantidad = inventario.cantidad
        db.commit()
        db.refresh(actualizar)

        return {"mensaje": "Inventario actualizado correctamente"}

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error al actualizar inventario: {str(e)}"
        )
    finally:
        db.close()


# ── ELIMINAR INVENTARIO ───────────────────────────────────────────────────
@router.delete("/{id_inventario}", summary="Eliminar ítem del inventario")
def eliminarInventario(id_inventario: int):
    """Elimina un registro del inventario del sistema."""
    db = SessionLocal()
    try:
        eliminar = db.query(Inventario).filter(
            Inventario.id_inventario == id_inventario
        ).first()

        if not eliminar:
            raise HTTPException(
                status_code=404,
                detail="Inventario no encontrado"
            )

        db.delete(eliminar)
        db.commit()

        return {"mensaje": "Inventario eliminado correctamente"}

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error al eliminar inventario: {str(e)}"
        )
    finally:
        db.close()

@router.get("/grafica/{id_usuario}")
def obtener_grafica(id_usuario: int):

    db = SessionLocal()

    actualizar_estados(db)

    try:

        resultado = (
            db.query(
                Categoria.nombre.label("categoria"),
                Estado.nombre.label("estado"),
                func.sum(Inventario.cantidad).label("cantidad")
            )
            .join(
                Producto,
                Producto.id_producto == Inventario.producto_id
            )
            .join(
                Categoria,
                Categoria.id_categoria == Producto.categoria_id
            )
            .join(
                Estado,
                Estado.id_estado == Inventario.estado_id
            )
            .filter(
                Inventario.usuario_id == id_usuario
            )
            .group_by(
                Categoria.nombre,
                Estado.nombre
            )
            .all()
        )

        return [
            {
                "categoria": item.categoria,
                "estado": item.estado,
                "cantidad": item.cantidad
            }
            for item in resultado
        ]

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

    finally:
        db.close()

