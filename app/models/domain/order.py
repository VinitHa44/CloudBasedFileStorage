from typing import List
from datetime import datetime

class OrderItem:  
    def __init__(self, product_id: str, quantity: int, price: float):
        self.product_id = product_id
        self.quantity = quantity
        self.price = price

class Order:  
    def __init__(self, user_id: str, items: List[OrderItem], total_amount: float, status: str, created_at: datetime = None, updated_at: datetime = None):
        self.user_id = user_id
        self.items = items
        self.total_amount = total_amount
        self.status = status  # "pending", "shipped", "delivered", "cancelled"
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
