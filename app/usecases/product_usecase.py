from datetime import datetime
import random
from fastapi import HTTPException
import httpx
import requests
from app.repositories.product_repository import ProductRepository
from app.models.domain.product import Product
from bson import ObjectId

from app.utils.gd_utils import upload_file_to_drive

class ProductUseCase:
    DUMMYJSON_URL = "https://dummyjson.com/products"

    @staticmethod
    async def preload_products(predefined_seller_ids: list):
        async with httpx.AsyncClient() as client:
            response = await client.get(ProductUseCase.DUMMYJSON_URL)
            products = response.json().get("products", [])

        for product in products:
            random_seller_id = random.choice(predefined_seller_ids)
            new_product = Product(
                title=product["title"],
                description=product["description"],
                category=product["category"],
                price=product["price"],
                rating=product["rating"],
                brand=product.get("brand", "Unknown"),
                images=product["images"],
                thumbnail=product["thumbnail"],
                seller_id=random_seller_id
            )
            await ProductRepository.insert_product(new_product.__dict__)

        return {"message": f"{len(products)} products preloaded successfully"}
    
    # @staticmethod
    # async def get_all_products():
    #     return await ProductRepository.get_all_products()

    # @staticmethod
    # async def get_product_by_id(product_id: str):
    #     product = await ProductRepository.get_product_by_id(product_id)
    #     if not product:
    #         return {"error": "Product not found"}
    #     return product

    # @staticmethod
    # async def update_product(product_id: str, update_data: dict, seller_id: str):
    #     product = await ProductRepository.get_product_by_id(product_id)
    #     if not product or product["seller_id"] != ObjectId(seller_id):
    #         return {"error": "Unauthorized or product not found"}
    #     await ProductRepository.update_product(product_id, update_data)
    #     return {"message": "Product updated successfully"}

    # @staticmethod
    # async def delete_product(product_id: str, seller_id: str):
    #     product = await ProductRepository.get_product_by_id(product_id)
    #     if not product or product["seller_id"] != ObjectId(seller_id):
    #         return {"error": "Unauthorized or product not found"}
    #     await ProductRepository.delete_product(product_id)
    #     return {"message": "Product deleted successfully"}


    @staticmethod
    async def create_product(product_data: dict, seller_id: str):
        try:
            # file_drive = await upload_file_to_drive(file)
            # file_url = f"https://drive.google.com/file/d/{file_drive['id']}/view"
            product_data["seller_id"] = ObjectId(seller_id)
            product = Product(**product_data)
            created_product = await ProductRepository.create_product(product)

            if not created_product:
                return {"error": "Failed to create product"}

            return created_product
    
        except Exception as e:
            raise HTTPException(status_code=500, detail="Internal Server Error")
        
    @staticmethod
    async def get_all_products():
        return await ProductRepository.get_all_products()