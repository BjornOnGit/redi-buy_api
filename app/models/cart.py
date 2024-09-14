from odmantic import Model, Field
from typing import List, Optional
from bson import ObjectId
from datetime import datetime
from pydantic import BaseModel

class CartItem(Model):
    product_id: ObjectId
    quantity: int

class Cart(Model):
    user_id: ObjectId
    items: List[CartItem] = []
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

class CartItemRequest(BaseModel):
    product_id: str
    quantity: int

class UpdateCartItem(Model):
    quantity: int