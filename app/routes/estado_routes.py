from fastapi import APIRouter, HTTPException, status
from app.database.database import SessionLocal
from app.models.estado import Estado
from app.schemas.estado_schema import EstadoCreate

router = APIRouter(
    prefix="/estados",
    tags=["Estados"]
)

# =========================
# LISTAR ESTADOS
# =========================
@router.get("/")
def listaEstado():
    db = SessionLocal()
    try:
        estados = db.query(Estado).all()
        return estados
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al obtener estados: {str(e)}"
        )
    finally:
        db.close()


# =========================
# CREAR ESTADO
# =========================
@router.post("/", status_code=status.HTTP_201_CREATED)
def crearEstado(estado: EstadoCreate):
    db = SessionLocal()
    try:
        nueva_estado = Estado(nombre=estado.nombre)
        db.add(nueva_estado)
        db.commit()
        db.refresh(nueva_estado)

        return {
            "mensaje": "Estado creado correctamente",
            "data": nueva_estado
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error al crear estado: {str(e)}"
        )
    finally:
        db.close()


# =========================
# OBTENER POR ID
# =========================
@router.get("/{id_estado}")
def obtenerEstadoId(id_estado: int):
    db = SessionLocal()
    try:
        estado = db.query(Estado).filter(
            Estado.id_estado == id_estado
        ).first()

        if not estado:
            raise HTTPException(
                status_code=404,
                detail="Estado no encontrado"
            )

        return estado

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al obtener estado: {str(e)}"
        )
    finally:
        db.close()


# =========================
# ACTUALIZAR ESTADO
# =========================
@router.put("/{id_estado}")
def actualizarEstado(id_estado: int, estado: EstadoCreate):
    db = SessionLocal()
    try:
        actualizar = db.query(Estado).filter(
            Estado.id_estado == id_estado
        ).first()

        if not actualizar:
            raise HTTPException(
                status_code=404,
                detail="Estado no encontrado"
            )

        actualizar.nombre = estado.nombre
        db.commit()
        db.refresh(actualizar)

        return {"mensaje": "Estado actualizado correctamente"}

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error al actualizar estado: {str(e)}"
        )
    finally:
        db.close()


# =========================
# ELIMINAR ESTADO
# =========================
@router.delete("/{id_estado}")
def eliminarEstado(id_estado: int):
    db = SessionLocal()
    try:
        eliminar = db.query(Estado).filter(
            Estado.id_estado == id_estado
        ).first()

        if not eliminar:
            raise HTTPException(
                status_code=404,
                detail="Estado no encontrado"
            )

        db.delete(eliminar)
        db.commit()

        return {"mensaje": "Estado eliminado correctamente"}

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error al eliminar estado: {str(e)}"
        )
    finally:
        db.close()