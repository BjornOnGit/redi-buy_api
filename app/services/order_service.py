from ..utils.database import get_engine
from bson import ObjectId
from fastapi import HTTPException
from datetime import datetime
from typing import List, Dict
from pydantic import EmailStr
from ..models import Order, OrderItem, PaymentInfo


class OrderService:
    async def create_order(user_id: ObjectId, email: EmailStr, items: List[OrderItem], shipping_address: Dict[str, str], payment_info: PaymentInfo):
        engine = await get_engine()
        total_amount = sum([item.price * item.quantity for item in items])
        order = Order(
            user_id=user_id,
            email=email,
            items=items,
            total_amount=total_amount,
            payment_info=payment_info,
            shipping_address=shipping_address
        )
        await engine.save(order)
        from ..celery_app import send_order_confirmation, create_invoice
        send_order_confirmation.delay(str(order.id))
        create_invoice.delay(str(order.id))
        return order

    async def get_orders(user_id: str):
        engine = await get_engine()
        orders = await engine.find(Order, Order.user_id == ObjectId(user_id))
        return orders

    async def get_order_by_id(order_id: str):
        engine = await get_engine()
        order = await engine.find_one(Order, Order.id == ObjectId(order_id))
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        return order


    async def update_order_status(order_id: str, status: str):
        engine = await get_engine()
        order = await engine.find_one(Order, Order.id == ObjectId(order_id))
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        
        # if status == "paid" and (not order.payment_info or not order.payment_info.transaction_id):
        #     raise HTTPException(
        #     status_code=400, 
        #     detail="Cannot mark order as 'paid' without a transaction_id"
        # )
    
        order.status = status
        order.updated_at = datetime.now()
        await engine.save(order)
        return order
    
    async def save_order(order: Order):
        engine = await get_engine()
        await engine.save(order)