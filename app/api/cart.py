from fastapi import APIRouter, Depends, HTTPException, status
from ..utils.database import get_engine
from typing import List
from bson import ObjectId
from ..services.cart_service import CartService
from app.models.cart import Cart, CartItemRequest, UpdateCartItem
from app.utils.auth import get_current_user

import structlog

logger = structlog.get_logger()

router = APIRouter()

@router.get("/cart", response_model=Cart)
async def get_cart(user = Depends(get_current_user)):
    engine = await get_engine()
    cart = await CartService.get_cart_by_user_id(user.id)
    logger.info("Current cart retrieved successfully")
    return cart

@router.post("/cart/add")
async def add_to_cart(item: CartItemRequest, user = Depends(get_current_user)):
    engine = await get_engine()
    if item.quantity <= 0:
        logger.error("Quantity must be greater than 0")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Quantity must be greater than 0")
    new_cart = await CartService.add_item_to_cart(user.id, item.product_id, item.quantity)
    logger.info("New cart added successfully")
    return new_cart

@router.put("/cart/update")
async def update_cart(item: CartItemRequest, updated_data: UpdateCartItem, user = Depends(get_current_user)):
    if item.quantity <= 0:
        logger.error("Quantity must be greater than 0")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Quantity must be greater than 0")
    
    updated_cart = await CartService.update_item_in_cart(user.id, item.product_id, updated_data)

    logger.info("Cart has been updated successfully")

    # Customize response format here
    response_data = {
        "user_id": str(updated_cart.user_id),
        "items": [{"product_id": str(i.product_id), "quantity": i.quantity} for i in updated_cart.items],
        "updated_at": updated_cart.updated_at,
    }

    return response_data


@router.delete("/cart/remove/{product_id}")
async def remove_from_cart(product_id: str, user = Depends(get_current_user)):
    engine = await get_engine()
    # try:
    #     product_id = ObjectId(product_id)
    # except:
    #     logger.error("Invalid product ID format")
    #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid product ID format")
    altered_cart = await CartService.remove_item_from_cart(user.id, product_id)
    if not altered_cart:
        logger.error("Product not found in cart")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found in cart")
    logger.info("Cart has been updated successfully")
    return  altered_cart
