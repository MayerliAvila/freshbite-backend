from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database.database import Base, engine

# Importar todos los modelos para que SQLAlchemy los registre
from app.models.producto import Producto
from app.models.usuario import Usuario
from app.models.categoria import Categoria
from app.models.inventario import Inventario
from app.models.estado import Estado

# Importar todos los routers
from app.routes.producto_routes import router as producto_router
from app.routes.usuario_routes import router as usuario_router
from app.routes.categoria_routes import router as categoria_router
from app.routes.inventario_routes import router as inventario_router
from app.routes.estado_routes import router as estado_router
from app.routes.ai_routes import router as ia_routes

# ─────────────────────────────────────────────
#  Metadatos para Swagger UI / OpenAPI
# ─────────────────────────────────────────────
description = """
## 🥗 FreshBite API

API REST para la gestión de inventario de alimentos frescos, usuarios, recetas y movimientos de stock.

### Módulos disponibles

| Módulo          | Descripción                                        |
|-----------------|----------------------------------------------------|
| **Usuarios**    | Registro, login y gestión de cuentas               |
| **Categorías**  | Clasificación de productos alimenticios            |
| **Productos**   | Catálogo de productos por categoría                |
| **Inventario**  | Control de stock con fechas de vencimiento         |
| **Estados**     | Estados del inventario (fresco, próximo a vencer…) |
| **Recetas**     | Recetas y sus ingredientes asociados               |

### Cómo probar
1. Expande un endpoint haciendo clic sobre él.
2. Haz clic en **Try it out**.
3. Completa los campos y presiona **Execute**.
"""

tags_metadata = [
    {
        "name": "Usuarios",
        "description": "Registro de usuarios, login y operaciones CRUD. Incluye autenticación básica por correo y contraseña.",
    },
    {
        "name": "Categorías",
        "description": "Gestión de categorías para clasificar los productos del inventario (p. ej. Lácteos, Frutas, Verduras).",
    },
    {
        "name": "Productos",
        "description": "Catálogo de productos disponibles. Cada producto pertenece a una categoría.",
    },
    {
        "name": "Inventario",
        "description": "Control del stock personal de cada usuario: cantidades, fechas de registro y vencimiento.",
    },
    {
        "name": "Estados",
        "description": "Estados que puede tener un ítem del inventario (Fresco, Próximo a vencer, Vencido, etc.).",
    },
    {
        "name": "Sugerencia",
        "description": "Lista de las recetas sugeridas por la IA en base de la tabla de ingrediente.",
    }
]

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="🥗 FreshBite API",
    description=description,
    version="1.0.0",
    openapi_tags=tags_metadata,
    contact={
        "name": "Equipo FreshBite",
        "email": "soporte@freshbite.app",
    },
    license_info={
        "name": "MIT",
    },
    docs_url="/docs",       # Swagger UI  →  http://localhost:8000/docs
    redoc_url="/redoc",     # ReDoc       →  http://localhost:8000/redoc
)

# ─────────────────────────────────────────────
#  CORS (para pruebas desde el frontend / Swagger)
# ─────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─────────────────────────────────────────────
#  Registrar todos los routers
# ─────────────────────────────────────────────
app.include_router(usuario_router)
app.include_router(categoria_router)
app.include_router(producto_router)
app.include_router(inventario_router)
app.include_router(estado_router)
app.include_router(ia_routes)


@app.get("/", tags=["Root"], summary="Health check")
def root():
    """Verifica que la API esté corriendo correctamente."""
    return {
        "status": "ok",
        "mensaje": "FreshBite API está funcionando ✅",
        "docs": "/docs",
        "redoc": "/redoc",
    }