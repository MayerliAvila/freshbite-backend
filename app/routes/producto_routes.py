from fastapi import APIRouter, HTTPException, status
from app.database.database import SessionLocal
from app.models.producto import Producto
from app.schemas.producto_schema import *

router = APIRouter(
    prefix="/productos",
    tags=["Productos"]
)

# ── LISTAR PRODUCTOS ──────────────────────────────────────────────────────────
@router.get("/", summary="Listar todos los productos")
def listaCategoria():
    """Retorna la lista completa de productos registrados en el catálogo."""
    db=SessionLocal()
    try:
        productos = db.query(Producto).all()
        return productos
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al obtener prodcutos: {str(e)}"
        )
    finally:
        db.close()

# ── CREAR PRODUCTO ───────────────────────────────────────────────────────────
@router.post("/", status_code=status.HTTP_201_CREATED, summary="Crear un nuevo producto")
def crearProducto(producto : ProductoCreate):
    """Crea un nuevo producto en el catálogo asociándolo a una categoría existente."""
    db = SessionLocal()
    try:
        nuevo_producto = Producto(
            nombre = producto.nombre, 
            categoria_id= producto.categoria_id
        )
        db.add(nuevo_producto)
        db.commit()
        db.refresh(nuevo_producto)
        return {
            "mensaje":"Producto creado correctamente",
            "data": nuevo_producto
        }
    except Exception as e:
        db.rollback()
        raise HTTPException (
            status_code= 500,
            detail=f"Error al crear Producto: {str(e)}"
        )
    finally:
        db.close()

# ── OBTENER PRODUCTO POR ID ──────────────────────────────────────────────────
@router.get("/{id_producto}", summary="Obtener producto por ID")
def obtenerProductoId(id_producto:int):
    """Retorna los detalles de un producto específico dado su ID."""
    db = SessionLocal()
    try:
        producto = db.query(Producto).filter(
            Producto.id_producto == id_producto
        ).first()
        if not producto:
            raise HTTPException(
                status_code=404,
                detail="Producto no encontrado"
            )
        return producto
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail =f"Error al obtener producto: {str(e)}"
        )
    finally:
        db.close()

# ── ACTUALIZAR PRODUCTO ──────────────────────────────────────────────────────
@router.put("/{id_producto}", summary="Actualizar un producto")
def actualizarProducto(id_producto:int, producto:ProductoCreate):
    """Actualiza el nombre o la categoría de un producto existente."""
    db = SessionLocal()
    try:
        productoActualizar = db.query(Producto).filter(
            Producto.id_producto == id_producto
        ).first()
        if not productoActualizar:
            raise HTTPException(
                status_code=404,
                detail = "Producto no encontrado"
            )
        productoActualizar.nombre = producto.nombre
        productoActualizar.categoria_id = producto.categoria_id
        db.commit()
        db.refresh(productoActualizar)
        return {"mensaje":"Producto actualizado correctamente"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error al actualizar producto: {str(e)}"
        )
    finally:
        db.close()

# ── ELIMINAR PRODUCTO ────────────────────────────────────────────────────────
@router.delete("/{id_producto}", summary="Eliminar un producto")
def eliminarProducto(id_producto:int):
    """Elimina permanentemente un producto del catálogo por su ID."""
    db = SessionLocal()
    try: 
        eliminarProducto = db.query(Producto).filter(
            Producto.id_producto == id_producto
        ).first()
        if not eliminarProducto:
            raise HTTPException(
                status_code = 404,
                detail=f"Producto no encontrado"
            )
        db.delete(eliminarProducto)
        db.commit()
        return {"mensaje":"Producto eliminado correctamente"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error al eliminar el producto: {str(e)}"
        )
    finally:
        db.close()