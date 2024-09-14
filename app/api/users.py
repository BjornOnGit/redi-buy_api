from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from ..models.user import UserCreate, UserModel, UserUpdate
from ..services.user_service import UserService
from ..utils.auth import create_access_token, get_current_user

import structlog

logger = structlog.get_logger()

router = APIRouter()

@router.post("/users/register", response_model=UserModel)
async def register_user(user: UserCreate, user_service: UserService = Depends()):
    db_user = await user_service.get_user_by_username(user.username)
    if db_user:
        logger.error("Username already registered")
        raise HTTPException(status_code=400, detail="Username already registered")
    created_user = await user_service.create_user(user)
    logger.info("User registered successfully")
    return created_user

@router.post("/users/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), user_service: UserService = Depends()):
    user = await user_service.authenticate_user(form_data.username, form_data.password)
    if not user:
        logger.error("Incorrect username or password")
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": user.username})

    logger.info("Access token created successfully")
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/users/me", response_model=UserModel)
async def read_users_me(current_user: UserModel = Depends(get_current_user)):
    logger.info("Current user retrieved successfully")
    return current_user

@router.get("/users/{user_id}", response_model=UserModel, status_code=status.HTTP_200_OK)
async def get_product(user_id: str, user_service: UserService = Depends()):
    user = await user_service.get_product_by_id(user_id)
    if not user:
        logger.error("User not found")
        raise HTTPException(status_code=404, detail="User not found")
    logger.info("User retrieved successfully")
    return user

@router.patch("/users/me", response_model=UserModel)
async def update_user(
    user_update: UserUpdate,
    current_user: UserModel = Depends(get_current_user),
    user_service: UserService = Depends()
):
    if not user_update.model_dump(exclude_unset=True):
        logger.error("No data provided for update")
        raise HTTPException(status_code=400, detail="No data provided for update")
    updated_user = await user_service.update_user(current_user.username, user_update)
    if not updated_user:
        logger.error("User not found")
        raise HTTPException(status_code=404, detail="User not found")
    logger.info("Current user updated successfully")
    return updated_user

@router.delete("/users/me", response_model=dict)
async def delete_user(
    current_user: UserModel = Depends(get_current_user),
    user_service: UserService = Depends()
):
    deleted = await user_service.delete_user(current_user.username)
    if not deleted:
        logger.error("User not found")
        raise HTTPException(status_code=404, detail="User not found")
    logger.info("User successfully deleted")
    return {"detail": "User successfully deleted"}
