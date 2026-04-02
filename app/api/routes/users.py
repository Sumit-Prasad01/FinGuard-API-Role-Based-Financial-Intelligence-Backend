from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.db.session import get_db
from app.schemas.user import UserCreate, UserResponse
from app.services.user_service import create_user, get_users, get_user_by_id
from app.dependencies.roles import require_roles

from slowapi import Limiter
from slowapi.util import get_remote_address


router = APIRouter(prefix="/users", tags=["Users"])

limiter = Limiter(key_func=get_remote_address)


@router.post("/", response_model=UserResponse)
@limiter.limit("10/minute")   
async def create_user_api(
    request: Request,          
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_roles(["admin"]))
):
    return await create_user(db, user_data)


@router.get("/", response_model=List[UserResponse])
@limiter.limit("30/minute")   # moderate
async def get_all_users(
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_roles(["admin"]))
):
    return await get_users(db)


@router.get("/{user_id}", response_model=UserResponse)
@limiter.limit("30/minute")
async def get_user(
    request: Request,
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_roles(["admin"]))
):
    return await get_user_by_id(db, user_id)