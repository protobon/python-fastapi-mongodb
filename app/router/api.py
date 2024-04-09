from fastapi import APIRouter
from app.router.product import router as product

api_router = APIRouter(prefix="/api")

api_router.include_router(product)
