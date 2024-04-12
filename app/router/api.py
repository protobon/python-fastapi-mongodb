from fastapi import APIRouter, Depends
from app.router.product import router as product
from app.auth.firebase import get_user

api_router = APIRouter(prefix="/api",
                       dependencies=[Depends(get_user)],
                       responses={
                           404: {"description": "Not found"},
                           408: {"description": "Timeout"}
                       }
                       )

api_router.include_router(product)
