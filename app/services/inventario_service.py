from datetime import date
from app.models.inventario import Inventario

def actualizar_estados(db):

    inventarios = db.query(Inventario).all()

    for item in inventarios:

        dias_restantes = (
            item.fecha_vencimiento.date()
            - date.today()
        ).days

        if dias_restantes < 0:
            item.estado_id = 3

        elif dias_restantes <= 3:
            item.estado_id = 2

        else:
            item.estado_id = 1

    db.commit()