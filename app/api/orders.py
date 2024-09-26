from fastapi import APIRouter, Depends, HTTPException, status
from ..utils.database import get_engine
from typing import List, Dict
from bson import ObjectId
from ..models.order import OrderItem, PaymentInfo, Order
from ..services.order_service import OrderService
from ..models.user import UserModel
from ..utils.auth import is_admin_or_seller, get_current_user

router = APIRouter()

@router.post("/orders", response_model=Order, status_code=status.HTTP_201_CREATED)
async def create_order(
    items: List[OrderItem], 
    shipping_address: Dict[str, str],
    payment_info: PaymentInfo, 
    user=Depends(get_current_user),
    engine=Depends(get_engine)
):
    try:
        order = await OrderService.create_order(user.id, user.email, items, shipping_address, payment_info)
        return order
    except:
        raise HTTPException(status_code=400, detail="Bad Order Request")


@router.get("/orders", response_model=List[Order], status_code=status.HTTP_200_OK)
async def get_orders(user=Depends(get_current_user), engine=Depends(get_engine)):
    orders = await OrderService.get_orders(user.id)
    return orders


@router.get("/orders/{order_id}", response_model=Order, status_code=status.HTTP_200_OK)
async def get_order(order_id: str, engine=Depends(get_engine)):
    try:
        order = await OrderService.get_order_by_id(order_id)
        return order
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/orders/{order_id}/status", response_model=Order, status_code=status.HTTP_200_OK)
async def update_order_status(order_id: str, status: str, user: UserModel = Depends(is_admin_or_seller), engine=Depends(get_engine)):
    if not user.is_admin_or_seller:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You don't have permission to update the order status.")
    
    order = await OrderService.update_order_status(order_id, status)
    return order