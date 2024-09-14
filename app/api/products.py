from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from ..models.product import ProductModel, UpdateProductModel
from ..models.user import UserModel
from ..utils.auth import is_admin_or_seller
from ..services.product_service import ProductService
from bson import ObjectId
import structlog

logger = structlog.get_logger()

router = APIRouter()

@router.get("/products", response_model=List[ProductModel], status_code=status.HTTP_200_OK)
async def get_products(skip: int = 0, limit: int = 10, product_service: ProductService = Depends()):
    logger.info("Products retrieved successfully")
    return await product_service.get_products(skip, limit)

@router.get("/products/{product_id}", response_model=ProductModel, status_code=status.HTTP_200_OK)
async def get_product(product_id: str, product_service: ProductService = Depends()):
    product = await product_service.get_product_by_id(product_id)
    if not product:
        logger.error("Product not found")
        raise HTTPException(status_code=404, detail="Product not found")
    logger.info("Product retrieved successfully")
    return product

@router.post("/products", response_model=ProductModel, status_code=status.HTTP_201_CREATED)
async def create_product(product: ProductModel, user: UserModel = Depends(is_admin_or_seller), product_service: ProductService = Depends()):
    logger.info("Product created successfully")
    return await product_service.create_product(product)

@router.delete("/products/{product_id}", response_model=ProductModel, status_code=status.HTTP_200_OK)
async def delete_product(product_id: str, product_service: ProductService = Depends(), user: UserModel = Depends(is_admin_or_seller)):
    product = await product_service.get_product_by_id(product_id)
    if not product:
        logger.error("Product not found")
        raise HTTPException(status_code=404, detail="Product not found")
    is_deleted = await product_service.delete_product(product_id)
    if not is_deleted:
        logger.error("Failed to delete product")
        raise HTTPException(status_code=500, detail="Failed to delete product")
    
    return product

@router.put("/products/{product_id}", response_model=ProductModel, status_code=status.HTTP_200_OK)
async def update_product(product_id: str, update_data: UpdateProductModel, product_service: ProductService = Depends(), user: UserModel = Depends(is_admin_or_seller)):
    updated_product = await product_service.update_product(product_id, update_data)
    logger.info("Product updated successfully")
    return updated_product
