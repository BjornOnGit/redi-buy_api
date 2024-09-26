from odmantic import Model, Field, ObjectId
from typing import List, Optional
from datetime import datetime

class Invoice(Model):
    order_id: ObjectId
    invoice_number: str = Field(unique=True)
    total_amount: float
    created_at: datetime = Field(default_factory=datetime.now)