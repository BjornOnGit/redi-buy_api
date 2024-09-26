from fastapi import APIRouter, Depends, HTTPException, status
from ..utils.auth import get_current_user
from ..utils.cache import redis_client
from fastapi.encoders import jsonable_encoder
from ..services.recommendation_service import recommend_products_for_user


router = APIRouter()

@router.get("/recommendations", status_code=status.HTTP_200_OK)
async def get_recommendations(user=Depends(get_current_user)):
    # Check if recommendations are cached
    recommendations = redis_client.get(f"user:{user.id}:recommendations")
    if recommendations:
        return jsonable_encoder(recommendations)
    
    # Fallback to synchronous recommendation generation
    recommended_products = await recommend_products_for_user(user.id)
    return jsonable_encoder(recommended_products)
