from odmantic import ObjectId
from ..utils.database import get_engine
from ..models.recommendation import Purchase, ProductView


async def recommend_products_for_user(user_id: ObjectId):
    engine = await get_engine()

    # Get the products the user has already purchased
    user_purchases = await engine.find(Purchase, Purchase.user_id == user_id)
    purchased_product_ids = {purchase.product_id for purchase in user_purchases}

    # Find other users who purchased the same products
    similar_users_purchases = await engine.find(
        Purchase, Purchase.product_id.in_(purchased_product_ids)
    )

    # Collect all the products purchased by similar users, excluding products the current user already purchased
    similar_user_product_ids = {purchase.product_id for purchase in similar_users_purchases}
    recommended_product_ids = similar_user_product_ids - purchased_product_ids

    # Fetch and return product recommendations
    recommended_products = await engine.find(ProductView, ProductView.id.in_(recommended_product_ids))
    return recommended_products
