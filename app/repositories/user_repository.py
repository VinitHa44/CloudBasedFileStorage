from app.models.domain.user import User
from app.config.database import db

class UserRepository:
    @staticmethod
    async def get_user_by_email(email: str):
        return await db.db["users"].find_one({"email": email})

    @staticmethod
    async def create_user(user: User):
        user_dict = user.__dict__
        result = await db.db["users"].insert_one(user_dict)
        return str(result.inserted_id)
