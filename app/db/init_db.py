from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.models import Role


async def seed_roles(db: AsyncSession):
    roles = ["admin", "analyst", "viewer"]

    for role_name in roles:
        result = await db.execute(select(Role).where(Role.name == role_name))
        existing = result.scalar_one_or_none()

        if not existing:
            db.add(Role(name=role_name))

    await db.commit()