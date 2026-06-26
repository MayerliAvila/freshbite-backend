from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.database.database import Base

class Categoria(Base):
    """Modelo ORM que representa la tabla 'categorias' en la base de datos."""

    __tablename__ = "categorias"

    id_categoria = Column(Integer, primary_key=True, index=True)  # Clave primaria autoincremental
    nombre       = Column(String, nullable=False)                  # Nombre de la categoría, obligatorio