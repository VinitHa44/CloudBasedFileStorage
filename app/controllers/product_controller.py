import json
import os
from typing import Annotated
from bson import ObjectId
from fastapi import APIRouter, Depends, Form, HTTPException, UploadFile, File
from app.usecases.product_usecase import ProductUseCase
from app.models.schemas.product_schema import ProductResponse
from app.utils.auth_utils import get_current_user 
import shutil

from app.utils.gd_utils import upload_to_google_drive

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

@router.post("/upload/")
async def upload_product_file(file: UploadFile = File(...), user: dict = Depends(get_current_user)):
    if user["role"] != "seller":
        raise HTTPException(status_code=403, detail="Only sellers can upload files")

    file_path = f"temp/{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    drive_link = await upload_to_google_drive(file_path, file.filename)
    os.remove(file_path)  # Clean up local file

    return {"message": "File uploaded successfully", "drive_link": drive_link}

@router.post("/", response_model=ProductResponse)
async def create_product(file: UploadFile = File(...),
    product_data: str = Form(...),  # Expecting JSON string
    user: dict = Depends(get_current_user),):
    if user["role"] != "seller":
        raise HTTPException(status_code=403, detail="Only sellers can add products")

    try:
        print(f"Received product_data: {product_data}")  # Debugging
        product_dict = json.loads(product_data)  # Convert string to dictionary
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON format in product_data")

    return await ProductUseCase.create_product(product_dict, file, user["id"])

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