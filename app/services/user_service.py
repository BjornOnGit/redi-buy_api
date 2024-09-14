from ..models.user import UserModel, UserCreate, UserInDB, UserUpdate
from ..utils.database import get_engine
from ..utils.auth import get_password_hash, verify_password
from datetime import datetime
from typing import Optional
from bson import ObjectId
class UserService:
    async def create_user(self, user: UserCreate) -> UserModel:
        engine = await get_engine()
        hashed_password = get_password_hash(user.password)
        user_in_db = UserModel(**user.model_dump(), password_hash=hashed_password)
        created_user = await engine.save(user_in_db)
        return created_user
    
    

    async def get_user_by_username(self, username: str) -> UserModel:
        engine = await get_engine()
        user = await engine.find_one(UserModel, UserModel.username == username)
        return user
    
    async def authenticate_user(self, username: str, password: str) -> UserModel:
        user = await self.get_user_by_username(username)
        if not user:
            return None
        if not verify_password(password, user.password_hash):
            return None
        return user
    
    async def get_product_by_id(self, user_id: str) -> Optional[UserModel]:
        engine = await get_engine()
        try:
            user = await engine.find_one(UserModel, UserModel.id == ObjectId(user_id))
            return user
        except:
            return None

    async def update_user(self, username: str, user_update: UserUpdate) -> UserModel:
        engine = await get_engine()
        user = await engine.find_one(UserModel, UserModel.username == username)
        if not user:
            return None
        
        updated_data = user_update.model_dump(exclude_unset=True)
        for key, value in updated_data.items():
            setattr(user, key, value)

        user.updated_at = datetime.now()
        await engine.save(user)
        return user
    
    async def delete_user(self, username: str) -> bool:
        engine = await get_engine()
        user = await engine.find_one(UserModel, UserModel.username == username)
        if not user:
            return False
        
        await engine.delete(user)
        return True