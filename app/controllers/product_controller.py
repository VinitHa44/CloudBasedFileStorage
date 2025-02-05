from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from app.usecases.product_usecase import ProductUseCase
from app.models.schemas.product_schema import ProductResponse
from app.utils.auth_utils import get_current_user 
import shutil

router = APIRouter()

@router.post("/preload-products/", response_model=dict)
async def preload_products():
    predefined_seller_ids = [
        str(ObjectId("67a36a669243387ce0f5cbef")), 
        str(ObjectId("67a36a739243387ce0f5cbf0")),
        str(ObjectId("67a36d635c6800c3fdc06c4d"))
    ]
    response = await ProductUseCase.preload_products(predefined_seller_ids)
    return response

@router.post("/", response_model=ProductResponse)
async def create_product(
    product_data: dict, 
    user: dict = Depends(get_current_user)  
):
    if user["role"] != "seller":
        raise HTTPException(status_code=403, detail="Only sellers can add products")
    return await ProductUseCase.create_product(product_data, user["id"])

@router.put("/{product_id}")
async def update_product(
    product_id: str, 
    update_data: dict, 
    user: dict = Depends(get_current_user)
):
    if user["role"] != "seller":
        raise HTTPException(status_code=403, detail="Only sellers can update products")
    response = await ProductUseCase.update_product(product_id, update_data, user["id"])
    if "error" in response:
        raise HTTPException(status_code=403, detail=response["error"])
    return response

@router.delete("/{product_id}")
async def delete_product(
    product_id: str, 
    user: dict = Depends(get_current_user)
):
    if user["role"] != "seller":
        raise HTTPException(status_code=403, detail="Only sellers can delete products")
    response = await ProductUseCase.delete_product(product_id, user["id"])
    if "error" in response:
        raise HTTPException(status_code=403, detail=response["error"])
    return response