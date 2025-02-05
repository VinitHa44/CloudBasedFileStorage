from datetime import datetime

class Complaint:  
    def __init__(self, user_id: str, order_id: str, product_id: str, issue: str, image_url: str, status: str = "open", created_at: datetime = None, updated_at: datetime = None):
        self.user_id = user_id
        self.order_id = order_id
        self.product_id = product_id
        self.issue = issue
        self.image_url = image_url
        self.status = status  # "open", "rejected"
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
