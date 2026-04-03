from fastapi import Depends, HTTPException, status

from app.dependencies.auth import get_current_user
from app.db.models import User


ROLE_MAP = {
    1: "admin",
    2: "analyst",
    3: "viewer"
}

def require_roles(allowed_roles: list[str]):
    async def role_checker(current_user=Depends(get_current_user)):
        user_role = ROLE_MAP.get(current_user.role_id)

        if user_role not in allowed_roles:
            raise HTTPException(status_code=403, detail="Forbidden")

        return current_user

    return role_checker