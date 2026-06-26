from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from app.database.database import Base

class Inventario(Base):
    """Modelo ORM que representa la tabla 'inventarios' en la base de datos."""

    __tablename__ = "inventarios"

    id_inventario     = Column(Integer, primary_key=True, index=True)                        # Clave primaria autoincremental
    usuario_id        = Column(Integer, ForeignKey("usuarios.id_usuario"),  nullable=False)  # Referencia al usuario dueño del inventario
    producto_id       = Column(Integer, ForeignKey("productos.id_producto"), nullable=False) # Referencia al producto registrado
    cantidad          = Column(Integer,  nullable=False)                                      # Cantidad disponible del producto
    fecha_ingreso     = Column(DateTime, nullable=False)                                      # Fecha en que se registró el producto
    fecha_vencimiento = Column(DateTime, nullable=False)                                      # Fecha de expiración del producto
    estado_id         = Column(Integer, ForeignKey("estados.id_estado"), nullable=False)     # Referencia al estado actual del producto