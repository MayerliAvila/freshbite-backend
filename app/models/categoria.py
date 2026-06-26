from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.database.database import Base

class Categoria(Base):
    __tablename__ = "categorias"
    id_categoria =Column(Integer, primary_key=True, index= True)
    nombre = Column(String, nullable=False)