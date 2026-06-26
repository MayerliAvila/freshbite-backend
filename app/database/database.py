"""
Módulo de configuración de la base de datos.

Establece la conexión con la base de datos mediante SQLAlchemy,
define la fábrica de sesiones y la clase base para los modelos ORM.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from dotenv import load_dotenv
import os

# Carga las variables de entorno definidas en el archivo .env
# Debe ejecutarse antes de cualquier llamada a os.getenv()
load_dotenv()

# URL de conexión a la base de datos obtenida desde las variables de entorno.
# Formato esperado: dialect+driver://user:password@host:port/dbname
# Ejemplo PostgreSQL: postgresql+psycopg2://user:pass@localhost:5432/mydb
DATABASE_URL = os.getenv("DATABASE_URL")

# Motor de conexión a la base de datos.
# pool_pre_ping=True verifica que la conexión siga activa antes de usarla,
# evitando errores por conexiones caídas o expiradas en el pool.
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# Fábrica de sesiones para interactuar con la base de datos.
#
# - autocommit=False: los cambios no se confirman automáticamente;
#   se requiere llamar a session.commit() de forma explícita.
# - autoflush=False:  los objetos pendientes no se sincronizan con la BD
#   antes de cada consulta; el flush se controla manualmente.
# - bind=engine:      asocia esta fábrica al motor de conexión definido arriba.
SessionLocal = sessionmaker(
    autocommit = False,
    autoflush  = False,
    bind       = engine
)

# Clase base de la que deben heredar todos los modelos ORM del proyecto.
# SQLAlchemy la usa para registrar las tablas y sus metadatos,
# lo que permite operaciones como Base.metadata.create_all(engine).
Base = declarative_base()