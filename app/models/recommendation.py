from odmantic import Model, Field, ObjectId
from datetime import datetime

class ProductView(Model):
    user_id: ObjectId
    product_id: ObjectId
    viewed_at: datetime = Field(default_factory=datetime.now)

class Purchase(Model):
    user_id: ObjectId
    product_id: ObjectId
    purchased_at: datetime = Field(default_factory=datetime.now)
