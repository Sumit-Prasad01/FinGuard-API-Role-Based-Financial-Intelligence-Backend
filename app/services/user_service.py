from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from app.db.models import User, Role
from app.schemas.user import UserCreate
from app.core.security import get_password_hash


async def create_user(db: AsyncSession, user_data: UserCreate):
    # Check if user already exists
    result = await db.execute(
        select(User).where(User.email == user_data.email)
    )
    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Assign default role(Viewer)
    role_result = await db.execute(
        select(Role).where(Role.name == "viewer")
    )
    role = role_result.scalar_one()

    # Create new user
    new_user = User(
        name=user_data.name,
        email=user_data.email,
        password=get_password_hash(user_data.password),
        role_id=role.id,
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return new_user


async def get_users(db: AsyncSession):
    result = await db.execute(select(User))
    return result.scalars().all()


async def get_user_by_id(db: AsyncSession, user_id: int):
    result = await db.execute(
        select(User).where(User.id == user_id)
    )
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return user