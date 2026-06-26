from sqlalchemy import Column, Integer, String,ForeignKey, DateTime
from sqlalchemy.orm import relationship

from app.database.database import Base

class Inventario(Base):
    __tablename__ = "inventarios"

    id_inventario=Column(Integer, primary_key= True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id_usuario"), nullable=False)
    producto_id = Column(Integer, ForeignKey("productos.id_producto"), nullable=False)
    cantidad= Column(Integer, nullable=False)
    fecha_ingreso = Column(DateTime, nullable=False)
    fecha_vencimiento = Column(DateTime, nullable=False)
    estado_id = Column(Integer, ForeignKey("estados.id_estado"), nullable=False)