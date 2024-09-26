import httpx
import os
from ..models.order import Order

PAYSTACK_SECRET_KEY = os.getenv('PAYSTACK_SECRET_KEY')
PAYSTACK_API_URL = os.getenv('PAYSTACK_API_URL')

class PaymentService:
    async def initialize_payment(self, order: Order):
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{PAYSTACK_API_URL}/transaction/initialize",
                json={
                    "amount": int(order.total_amount * 100),  # Amount in kobo
                    "email": order.email,
                    "reference": str(order.id)
                },
                headers={"Authorization": f"Bearer {PAYSTACK_SECRET_KEY}"}
            )
        return response.json()

    async def verify_payment(self, reference: str):
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(
                f"{PAYSTACK_API_URL}/transaction/verify/{reference}",
                headers={"Authorization": f"Bearer {PAYSTACK_SECRET_KEY}"}
            )
        return response.json()