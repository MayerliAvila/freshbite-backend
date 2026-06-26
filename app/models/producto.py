from sqlalchemy import Column,Integer,String,ForeignKey
from sqlalchemy.orm import relationship

from app.database.database import Base

class Producto(Base):

    __tablename__ = "productos"

    id_producto = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(250), nullable=False)
    categoria_id = Column(Integer, ForeignKey("categorias.id_categoria"), nullable=False)
