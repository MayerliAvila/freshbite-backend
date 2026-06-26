from pydantic import BaseModel
from datetime import date

class UsuarioCreate(BaseModel):
    nombre: str
    correo: str
    password: str

class UsuarioResponse(BaseModel):
    id_usuario: int
    nombre: str
    correo: str
    password: str
    fecha_registro: date

    class Config:
        from_attributes = True

class UsuarioLogin(BaseModel):
    correo: str
    password: str