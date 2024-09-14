from odmantic import Model, Field
from pydantic import EmailStr, BaseModel
from typing import Optional
from datetime import datetime


class UserModel(Model):
    username: str
    email: EmailStr
    password_hash: str
    role: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    address: Optional[dict[str, str]] = None
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    address: Optional[dict[str, str]] = None

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    role: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    address: Optional[dict] = None

class UserInDB(UserModel):
    pass
