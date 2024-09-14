from ..models.product import ProductModel, UpdateProductModel
from bson import ObjectId
from fastapi import HTTPException
from ..utils.database import get_engine
from typing import List, Optional
from datetime import datetime

class ProductService:
    async def get_products(self, skip: int = 0, limit: int = 10) -> List[ProductModel]:
        engine = await get_engine()

        products = await engine.find(ProductModel, skip=skip, limit=limit)
        return list(products)
    
    async def get_product_by_id(self, product_id: str) -> Optional[ProductModel]:
        engine = await get_engine()
        try:
            product = await engine.find_one(ProductModel, ProductModel.id == ObjectId(product_id))
            return product
        except:
            return None
    
    async def create_product(self, product: ProductModel) -> ProductModel:
        engine = await get_engine()

        await engine.save(product)
        return product
    
    async def delete_product(self, product_id: str) -> Optional[ProductModel]:
        engine = await get_engine()
        try:
            product = await engine.find_one(ProductModel, ProductModel.id == ObjectId(product_id))
            await engine.delete(product)
            return True
        except:
                return HTTPException(status_code=400, detail="Invalid product ID")
    
    async def update_product(self, product_id: str, update_data: UpdateProductModel) -> ProductModel:
        engine = await get_engine()
        
        product = await engine.find_one(ProductModel, ProductModel.id == ObjectId(product_id))
        
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        if update_data.name is not None:
            product.name = update_data.name
        if update_data.description is not None:
            product.description = update_data.description
        if update_data.price is not None:
            product.price = update_data.price
        if update_data.category is not None:
            product.category = update_data.category
        if update_data.stock is not None:
            product.stock = update_data.stock
        
        product.updated_at = datetime.now()
        
        await engine.save(product)
        
        return product