from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.database.database import Base

class Estado(Base):
    __tablename__ ="estados"

    id_estado=Column(Integer, primary_key=True, index=True)
    nombre=Column(String(30), nullable=False)