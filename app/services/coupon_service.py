from ..utils.database import get_engine
from ..models.coupon import Coupon
from bson import ObjectId
from fastapi import HTTPException
from datetime import datetime

class CouponService:
    
    async def create_coupon(coupon_code: str, discount_type: str, discount_value: float, valid_from: datetime, valid_to: datetime, usage_limit: int):
        engine = await get_engine()
        existing_coupon = await engine.find_one(Coupon, Coupon.coupon_code == coupon_code)
        if existing_coupon:
            raise HTTPException(status_code=400, detail="Coupon code already exists.")
        
        coupon = Coupon(
            coupon_code=coupon_code,
            discount_type=discount_type,
            discount_value=discount_value,
            valid_from=valid_from,
            valid_to=valid_to,
            usage_limit=usage_limit,
            used_count=0
        )
        await engine.save(coupon)
        return coupon

    async def apply_coupon(coupon_code: str):
        engine = await get_engine()
        coupon = await engine.find_one(Coupon, Coupon.coupon_code == coupon_code)
        if not coupon:
            raise HTTPException(status_code=404, detail="Coupon not found.")
        
        # Check if the coupon is within the valid date range
        if not (coupon.valid_from <= datetime.now() <= coupon.valid_to):
            raise HTTPException(status_code=400, detail="Coupon is not valid at this time.")
        
        # Check if usage limit has been reached
        if coupon.used_count >= coupon.usage_limit:
            raise HTTPException(status_code=400, detail="Coupon usage limit has been reached.")
        
        # Apply the coupon (you can include additional logic here for orders)
        coupon.used_count += 1
        await engine.save(coupon)
        return coupon
    
    async def get_coupons():
        engine = await get_engine()
        coupons = await engine.find(Coupon)
        return list(coupons)

    async def delete_coupon(coupon_id: str):
        engine = await get_engine()
        coupon = await engine.find_one(Coupon, Coupon.id == ObjectId(coupon_id))
        if not coupon:
            raise HTTPException(status_code=404, detail="Coupon not found.")
        await engine.delete(coupon)
