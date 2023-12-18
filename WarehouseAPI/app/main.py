from fastapi import FastAPI
from app.routes.suppliers import router as suppliers_router
from app.routes.warehouses import router as warehouses_router
from app.routes.items import router as items_router
from app.routes.shelves import router as shelves_router

app = FastAPI()
app.include_router(suppliers_router)
app.include_router(warehouses_router)
app.include_router(items_router)
app.include_router(shelves_router)
