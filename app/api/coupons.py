from fastapi import APIRouter, Depends, HTTPException, status, Body
from ..services.coupon_service import CouponService
from ..utils.auth import is_admin_or_seller
from datetime import datetime
from fastapi.encoders import jsonable_encoder
from ..models.coupon import ApplyCouponRequest

router = APIRouter()

# Apply coupon
@router.post("/coupons/apply", status_code=status.HTTP_200_OK)
async def apply_coupon(coupon_data: ApplyCouponRequest):
    coupon_code = coupon_data.coupon_code
    try:
        coupon = await CouponService.apply_coupon(coupon_code)
        return coupon
    except HTTPException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Coupon not found")

# Get all coupons (admin only)
@router.get("/coupons", status_code=status.HTTP_200_OK, dependencies=[Depends(is_admin_or_seller)])
async def get_coupons():
    coupons = await CouponService.get_coupons()
    return jsonable_encoder(coupons)

# Create a new coupon (admin only)
@router.post("/coupons", status_code=status.HTTP_201_CREATED, dependencies=[Depends(is_admin_or_seller)])
async def create_coupon(coupon_code: str = Body(...), discount_type: str = Body(...), discount_value: float = Body(...), valid_from: datetime= Body(...), valid_to: datetime = Body(...), usage_limit: int = Body(...)):
    try:
        return await CouponService.create_coupon(coupon_code, discount_type, discount_value, valid_from, valid_to, usage_limit)
    except HTTPException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Couldn't create coupon")

# Delete a coupon by ID (admin only)
@router.delete("/coupons/{coupon_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(is_admin_or_seller)])
async def delete_coupon(coupon_id: str):
    try:
        await CouponService.delete_coupon(coupon_id)
    except HTTPException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Couldn't delete coupon")
