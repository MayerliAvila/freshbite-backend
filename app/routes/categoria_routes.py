from fastapi import APIRouter, HTTPException, status
from app.database.database import SessionLocal
from app.models.categoria import Categoria
from app.schemas.categoria_schema import CategoriaCreate

router = APIRouter(
    prefix="/categorias",
    tags=["Categorias"]
)

# ── LISTAR CATEGORIAS ──────────────────────────────────────────────────
@router.get("/", summary="Listar todas las categorías")
def listaCategoria():
    """Retorna todas las categorías disponibles para clasificar productos."""
    db = SessionLocal()
    try:
        categorias = db.query(Categoria).all()
        return categorias
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al obtener categorías: {str(e)}"
        )
    finally:
        db.close()


# ── CREAR CATEGORIA ───────────────────────────────────────────────────
@router.post("/", status_code=status.HTTP_201_CREATED, summary="Crear una nueva categoría")
def crearCategoria(categoria: CategoriaCreate):
    """Agrega una nueva categoría al sistema (p. ej. Lácteos, Frutas, Carnes)."""
    db = SessionLocal()
    try:
        nueva_categoria = Categoria(nombre=categoria.nombre)
        db.add(nueva_categoria)
        db.commit()
        db.refresh(nueva_categoria)

        return {
            "mensaje": "Categoría creada correctamente",
            "data": nueva_categoria
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error al crear categoría: {str(e)}"
        )
    finally:
        db.close()


# ── OBTENER CATEGORIA POR ID ────────────────────────────────────────────
@router.get("/{id_categoria}", summary="Obtener categoría por ID")
def obtenerCategoriaId(id_categoria: int):
    """Retorna los datos de una categoría específica dado su ID."""
    db = SessionLocal()
    try:
        categoria = db.query(Categoria).filter(
            Categoria.id_categoria == id_categoria
        ).first()

        if not categoria:
            raise HTTPException(
                status_code=404,
                detail="Categoría no encontrada"
            )

        return categoria

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al obtener categoría: {str(e)}"
        )
    finally:
        db.close()


# ── ACTUALIZAR CATEGORIA ─────────────────────────────────────────────────
@router.put("/{id_categoria}", summary="Actualizar una categoría")
def actualizarCategoria(id_categoria: int, categoria: CategoriaCreate):
    """Modifica el nombre de una categoría existente."""
    db = SessionLocal()
    try:
        actualizar = db.query(Categoria).filter(
            Categoria.id_categoria == id_categoria
        ).first()

        if not actualizar:
            raise HTTPException(
                status_code=404,
                detail="Categoría no encontrada"
            )

        actualizar.nombre = categoria.nombre
        db.commit()
        db.refresh(actualizar)

        return {"mensaje": "Categoría actualizada correctamente"}

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error al actualizar categoría: {str(e)}"
        )
    finally:
        db.close()


# ── ELIMINAR CATEGORIA ──────────────────────────────────────────────────
@router.delete("/{id_categoria}", summary="Eliminar una categoría")
def eliminarCategoria(id_categoria: int):
    """Elimina una categoría del sistema. Asegúrate de que no tenga productos asociados."""
    db = SessionLocal()
    try:
        eliminar = db.query(Categoria).filter(
            Categoria.id_categoria == id_categoria
        ).first()

        if not eliminar:
            raise HTTPException(
                status_code=404,
                detail="Categoría no encontrada"
            )

        db.delete(eliminar)
        db.commit()

        return {"mensaje": "Categoría eliminada correctamente"}

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error al eliminar categoría: {str(e)}"
        )
    finally:
        db.close()