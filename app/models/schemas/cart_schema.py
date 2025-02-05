from pydantic import BaseModel

class CartItemResponse(BaseModel): 
    cart_id: str  
    user_id: str
    product_id: str
    quantity: int
