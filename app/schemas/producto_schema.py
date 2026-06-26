from pydantic import BaseModel

class ProductoCreate(BaseModel):
    nombre:str
    categoria_id:int

class ProductoResponse(BaseModel):
    id_producto:int
    nombre:str
    categoria_id:int

    class Config:
        from_attributes = True