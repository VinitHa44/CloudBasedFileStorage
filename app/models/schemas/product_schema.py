from typing import List
from pydantic import BaseModel

class ProductResponse(BaseModel): 
    product_id: str  
    title: str
    description: str
    category: str
    price: float
    rating: float
    brand: str
    images: List[str]
    thumbnail: str
    seller_id: str
