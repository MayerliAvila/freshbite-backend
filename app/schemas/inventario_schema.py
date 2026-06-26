from pydantic import BaseModel
from datetime import date

class InventarioCreate(BaseModel):
    usuario_id: int
    producto_id:int
    cantidad: int
    fecha_vencimiento:date
    estado_id:int

class InventarioResponse(BaseModel):
    id_inventario:int
    usuario_id: int
    producto_id:int
    cantidad: int
    fecha_registro:date
    fecha_vencimiento:date
    estado_id:int
    
    class Config:
        from_attributes:True

class InventarioEditar(BaseModel):
    cantidad: int