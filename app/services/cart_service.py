from ..utils.database import get_engine
from ..models import Cart, CartItem, ProductModel, UpdateCartItem
from bson import ObjectId
from fastapi import HTTPException
from typing import Optional
from datetime import datetime

import structlog

logger = structlog.get_logger()

class CartService:
    async def get_cart_by_user_id(user_id: ObjectId) -> Cart:
        engine = await get_engine()
        cart = await engine.find_one(Cart, Cart.user_id == user_id)
        if cart is None:
            cart = Cart(user_id=user_id, items=[])
            await engine.save(cart)
        return cart

    async def add_item_to_cart( user_id: ObjectId, product_id: str, quantity: int) -> Cart:
        engine = await get_engine()
        product = await engine.find_one(ProductModel, ProductModel.id == ObjectId(product_id))
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        cart = await CartService.get_cart_by_user_id(user_id)
        # logger.info(f"Cart  item added: {product_id} x {quantity}")
        for item in cart.items:
            if item.product_id == product_id:
                item.quantity += quantity
                await engine.save(cart)
                return cart
        cart.items.append(CartItem(product_id=product_id, quantity=quantity))
        await engine.save(cart)
        # logger.info(f"Cart saved: {cart}")
        return cart

    async def update_item_in_cart(user_id: ObjectId, product_id: str, updated_data: UpdateCartItem) -> Optional[Cart]:
        engine = await get_engine()

        # Check if product exists
        product = await engine.find_one(ProductModel, ProductModel.id == ObjectId(product_id))
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        # Get the user's cart
        cart = await CartService.get_cart_by_user_id(user_id)
        if cart is None:
            raise HTTPException(status_code=404, detail="Cart not found")

        # Look for the item in the cart and update its quantity
        item_found = False
        for item in cart.items:
            if str(item.product_id) == product_id:
                item.quantity = updated_data.quantity
                item_found = True
                break

        if not item_found:
            raise HTTPException(status_code=404, detail="Product not found in cart")

        # Update the `updated_at` timestamp
        cart.updated_at = datetime.now()

        # Save the updated cart
        await engine.save(cart)

        return cart


    async def remove_item_from_cart(user_id: ObjectId, product_id: str):
        engine = await get_engine()
        product = await engine.find_one(ProductModel, ProductModel.id == ObjectId(product_id))
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        cart = await CartService.get_cart_by_user_id(user_id)
        cart.items = [item for item in cart.items if item.product_id != product_id]
        await engine.save(cart)
        return cart
