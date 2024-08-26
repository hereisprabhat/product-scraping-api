from fastapi import APIRouter

from app.products import api as products_api

api_router = APIRouter()

api_router.include_router(products_api.router, prefix="/products")
