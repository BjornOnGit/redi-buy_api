from odmantic import Model, Field
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel

class Coupon(Model):
    coupon_code: str = Field(unique=True)
    discount_type: str
    discount_value: float
    valid_from: datetime
    valid_to: datetime
    usage_limit: int
    used_count: int = 0
    created_at:  datetime = Field(default_factory=datetime.now)
    updated_at:  datetime = Field(default_factory=datetime.now)

class ApplyCouponRequest(BaseModel):
    coupon_code: str