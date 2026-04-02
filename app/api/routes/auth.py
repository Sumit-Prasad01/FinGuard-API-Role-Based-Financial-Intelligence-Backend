from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.auth import LoginRequest, RefreshRequest, Token
from app.services.auth_service import authenticate_user, refresh_access_token
from app.schemas.user import UserCreate, UserResponse
from app.services.user_service import create_user


from slowapi import Limiter
from slowapi.util import get_remote_address


router = APIRouter(prefix="/auth", tags=["Auth"])

limiter = Limiter(key_func=get_remote_address)


# LOGIN
@router.post("/login", response_model=Token)
@limiter.limit("5/minute")
async def login(
    request: Request,
    login_data: LoginRequest,
    db: AsyncSession = Depends(get_db)
):
    return await authenticate_user(db, login_data)



# REFRESH TOKEN
@router.post("/refresh", response_model=Token)
@limiter.limit("10/minute")
async def refresh_token(
    request: Request,
    refresh_data: RefreshRequest
):
    return await refresh_access_token(refresh_data.refresh_token)


# REGISTER USER
@router.post("/register", response_model=UserResponse)
@limiter.limit("5/minute")
async def register(
    request: Request,
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    return await create_user(db, user_data)