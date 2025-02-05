from datetime import datetime

class CartItem:  
    def __init__(self, user_id: str, product_id: str, quantity: int, created_at: datetime = None, updated_at: datetime = None):
        self.user_id = user_id
        self.product_id = product_id
        self.quantity = quantity
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
