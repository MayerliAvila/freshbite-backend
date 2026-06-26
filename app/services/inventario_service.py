from datetime import date
from app.models.inventario import Inventario


def actualizar_estados(db):
    """
    Actualiza el estado de cada ítem del inventario según su fecha de vencimiento.

    Criterios aplicados:
    - Vencido         (estado_id=3): la fecha de vencimiento ya pasó (días restantes < 0).
    - Próximo a vencer(estado_id=2): vence en 3 días o menos.
    - Fresco          (estado_id=1): vence en más de 3 días.

    - **db**: Sesión activa de SQLAlchemy.
    """

    # Obtiene todos los registros del inventario
    inventarios = db.query(Inventario).all()

    for item in inventarios:

        # Calcula los días que faltan (o pasaron) respecto a la fecha actual
        dias_restantes = (
            item.fecha_vencimiento.date()
            - date.today()
        ).days

        if dias_restantes < 0:
            item.estado_id = 3    # Vencido

        elif dias_restantes <= 3:
            item.estado_id = 2    # Próximo a vencer

        else:
            item.estado_id = 1    # Fresco

    # Confirma todos los cambios de estado en la base de datos
    db.commit()