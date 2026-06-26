from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.database.database import Base

class Producto(Base):
    """Modelo ORM que representa la tabla 'productos' en la base de datos."""

    __tablename__ = "productos"

    id_producto  = Column(Integer,      primary_key=True, index=True)                       # Clave primaria autoincremental
    nombre       = Column(String(250),  nullable=False)                                      # Nombre del producto, máximo 250 caracteres
    categoria_id = Column(Integer,      ForeignKey("categorias.id_categoria"), nullable=False) # Referencia a la categoría del producto