from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.db.session import get_db
from app.schemas.user import UserCreate, UserResponse
from app.services.user_service import create_user, get_users, get_user_by_id
from app.dependencies.roles import require_roles


router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=UserResponse)
async def create_user_api(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_roles(["admin"]))  # Only admin
):
    return await create_user(db, user_data)


@router.get("/", response_model=List[UserResponse])
async def get_all_users(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_roles(["admin"]))  # Only admin
):
    return await get_users(db)


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_roles(["admin"]))
):
    return await get_user_by_id(db, user_id)