from pydantic import BaseModel

class ComplaintResponse(BaseModel): 
    complaint_id: str  
    user_id: str
    order_id: str
    product_id: str
    issue: str
    image_url: str
    status: str
