from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship

from app.database.database import Base

class Usuario(Base):
    """Modelo ORM que representa la tabla 'usuarios' en la base de datos."""

    __tablename__ = "usuarios"

    id_usuario      = Column(Integer,     primary_key=True, index=True)       # Clave primaria autoincremental
    nombre          = Column(String(255), nullable=False)                      # Nombre completo del usuario, máximo 255 caracteres
    correo          = Column(String(150), unique=True)                         # Correo electrónico único por usuario
    password        = Column(String(10),  nullable=False)                      # Contraseña del usuario, máximo 10 caracteres
    fecha_registro  = Column(DateTime,    nullable=False)                      # Fecha en que se registró el usuario