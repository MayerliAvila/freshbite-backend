from pydantic import BaseModel

class EstadoCreate(BaseModel):
    nombre:str

class EstadoResponse(BaseModel):
    id_estado:int
    nombre:str
    
    class Config:
        from_attributes=True
