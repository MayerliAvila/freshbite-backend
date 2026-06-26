from datetime import datetime

from fastapi import APIRouter, HTTPException, status
from app.database.database import SessionLocal
from app.models.usuario import Usuario
from app.schemas.usuario_schema import *

router = APIRouter(
    prefix="/usuarios",
    tags=["Usuarios"]
)

# ── LISTAR USUARIOS ──────────────────────────────────────────────────
@router.get("/", summary="Listar todos los usuarios")
def listaUsuario():
    """Retorna la lista completa de usuarios registrados en la plataforma."""
    db = SessionLocal()
    try:
        usuarios = db.query(Usuario).all()
        return usuarios
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al obtener usuarios: {str(e)}"
        )
    finally:
        db.close()

# ── REGISTRAR USUARIO ───────────────────────────────────────────────
@router.post("/", status_code=status.HTTP_201_CREATED, summary="Registrar un nuevo usuario")
def crearUsuario(usuario: UsuarioCreate):
    """Crea una cuenta nueva para un usuario con nombre, correo, contraseña y fecha de registro."""
    db = SessionLocal()
    try:
        nuevo_usuario = Usuario(
            nombre=usuario.nombre,
            correo=usuario.correo,
            password=usuario.password,
            fecha_registro=datetime.now()
        )
        db.add(nuevo_usuario)
        db.commit()
        db.refresh(nuevo_usuario)
        return {
            "mensaje": "Usuario creado correctamente",
            "data": nuevo_usuario
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error al crear usuario: {str(e)}"
        )
    finally:
        db.close()

# ── LOGIN ───────────────────────────────────────────────────────────────
@router.post("/login", summary="Iniciar sesión")
def loginUsuario(usuario: UsuarioLogin):
    """Autentica a un usuario por correo y contraseña. Retorna los datos del usuario si las credenciales son correctas."""
    db = SessionLocal()
    try:
        usuarioEncontrado = db.query(Usuario).filter(
            Usuario.correo == usuario.correo
        ).first()
        if not usuarioEncontrado:
            raise HTTPException(
                status_code=404,
                detail="Usuario no encontrado"
            )
        if usuarioEncontrado.password != usuario.password:
            raise HTTPException(
                status_code=401,
                detail="Contraseña incorrecta"
            )
        return {
            "mensaje": "Login exitoso",
            "data": usuarioEncontrado
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al autenticar usuario: {str(e)}"
        )
    finally:
        db.close()

# ── OBTENER USUARIO POR ID ─────────────────────────────────────────────────
@router.get("/{id_usuario}", summary="Obtener usuario por ID")
def obtenerUsuarioId(id_usuario: int):
    """Retorna los datos de un usuario específico identificado por su ID."""
    db = SessionLocal()
    try:
        usuario = db.query(Usuario).filter(
            Usuario.id_usuario == id_usuario
        ).first()
        if not usuario:
            raise HTTPException(
                status_code=404,
                detail="Usuario no encontrado"
            )
        return usuario
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al obtener usuario: {str(e)}"
        )
    finally:
        db.close()

# ── ACTUALIZAR USUARIO ───────────────────────────────────────────────────
@router.put("/{id_usuario}", summary="Actualizar datos del usuario")
def actualizarUsuario(id_usuario: int, usuario: UsuarioCreate):
    """Modifica el nombre, correo o contraseña de un usuario existente."""
    db = SessionLocal()
    try:
        usuarioActualizar = db.query(Usuario).filter(
            Usuario.id_usuario == id_usuario
        ).first()
        if not usuarioActualizar:
            raise HTTPException(
                status_code=404,
                detail="Usuario no encontrado"
            )
        usuarioActualizar.nombre = usuario.nombre
        usuarioActualizar.correo = usuario.correo
        usuarioActualizar.password = usuario.password
        db.commit()
        db.refresh(usuarioActualizar)
        return {"mensaje": "Usuario actualizado correctamente"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error al actualizar usuario: {str(e)}"
        )
    finally:
        db.close()

# ── ELIMINAR USUARIO ─────────────────────────────────────────────────────
@router.delete("/{id_usuario}", summary="Eliminar un usuario")
def eliminarUsuario(id_usuario: int):
    """Elimina permanentemente la cuenta de un usuario del sistema."""
    db = SessionLocal()
    try:
        eliminar = db.query(Usuario).filter(
            Usuario.id_usuario == id_usuario
        ).first()
        if not eliminar:
            raise HTTPException(
                status_code=404,
                detail="Usuario no encontrado"
            )
        db.delete(eliminar)
        db.commit()
        return {"mensaje": "Usuario eliminado correctamente"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error al eliminar el usuario: {str(e)}"
        )
    finally:
        db.close()