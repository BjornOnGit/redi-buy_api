from odmantic import Model, Field
from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class ProductModel(Model):
    name: str
    description: str
    price: float
    category: str
    stock: int
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    message: Optional[str] = None

class UpdateProductModel(Model):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    category: Optional[str] = None
    stock: Optional[int] = None