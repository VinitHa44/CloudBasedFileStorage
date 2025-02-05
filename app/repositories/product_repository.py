from app.config.database import db
from app.models.domain.product import Product
import random

class ProductRepository:

    @staticmethod
    async def insert_product(product_data: dict):
        result = await db.db["products"].insert_one(product_data)
        return str(result.inserted_id)
    
    # @staticmethod
    # async def preload_products(products: list):
    #     await db.db["products"].insert_many(products)

    @staticmethod
    async def create_product(product: Product):
        product_dict = product.__dict__
        result = await db.db["products"].insert_one(product_dict)
        
        created_product = await db.db["products"].find_one({"_id": result.inserted_id})
        
        if created_product:
            created_product["product_id"] = str(created_product.pop("_id"))  # Rename _id -> product_id
            created_product["seller_id"] = str(created_product["seller_id"])  # Convert ObjectId to string

            return created_product
        
        return None


    @staticmethod
    async def get_all_products():
        return await db.db["products"].find().to_list(100)

    @staticmethod
    async def get_product_by_id(product_id: str):
        return await db.db["products"].find_one({"_id": product_id})

    @staticmethod
    async def update_product(product_id: str, update_data: dict):
        return await db.db["products"].update_one({"_id": product_id}, {"$set": update_data})

    @staticmethod
    async def delete_product(product_id: str):
        return await db.db["products"].delete_one({"_id": product_id})
