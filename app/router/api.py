from fastapi import APIRouter
from app.router.product import product

api_router = APIRouter(prefix="/api")

api_router.include_router(product)
