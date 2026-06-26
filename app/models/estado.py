from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.database.database import Base

class Estado(Base):
    """Modelo ORM que representa la tabla 'estados' en la base de datos."""

    __tablename__ = "estados"

    id_estado = Column(Integer, primary_key=True, index=True)  # Clave primaria autoincremental
    nombre    = Column(String(30), nullable=False)              # Nombre del estado, máximo 30 caracteres