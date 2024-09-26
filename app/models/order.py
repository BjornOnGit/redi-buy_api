from odmantic import Model, Field, ObjectId
from typing import List, Optional
from pydantic import EmailStr
from datetime import datetime
from decimal import Decimal

class OrderItem(Model):
    product_id: ObjectId
    quantity: int
    price: float

class PaymentInfo(Model):
    payment_method: str
    transaction_id: Optional[str] = None


class Order(Model):
    user_id: ObjectId
    email: Optional[EmailStr] = None
    items: List[OrderItem]
    total_amount: float
    status: str = Field(default="pending")  # Status: pending, paid, shipped, delivered
    payment_info: Optional[PaymentInfo] = None
    shipping_address: Optional[dict[str, str]] = None
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
