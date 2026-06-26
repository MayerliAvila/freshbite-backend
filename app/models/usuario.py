from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship

from app.database.database import Base

class Usuario(Base):
    __tablename__ ="usuarios"

    id_usuario = Column(Integer, primary_key=True, index=True)
    nombre=Column(String(255),nullable=False)
    correo=Column(String(150), unique=True)
    password=Column(String(10),nullable=False)
    fecha_registro=Column(DateTime, nullable=False)