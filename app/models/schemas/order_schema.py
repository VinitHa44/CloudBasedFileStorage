from typing import List
from pydantic import BaseModel

class OrderItemResponse(BaseModel): 
    product_id: str  
    quantity: int
    price: float

class OrderResponse(BaseModel): 
    order_id: str  
    user_id: str
    items: List[OrderItemResponse]
    total_amount: float
    status: str
