from fastapi import APIRouter
from app.controllers.product_controller import router as pro_router

product_router = APIRouter()
product_router.include_router(pro_router, prefix="/products", tags=["Productss"])
