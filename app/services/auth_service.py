from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.db.models import User
from app.schemas.auth import LoginRequest
from app.core.security import verify_password, create_access_token


def authenticate_user(db: Session, login_data: LoginRequest):
    user = db.query(User).filter(User.email == login_data.email).first()

    if not user or not verify_password(login_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user"
        )

    # Create JWT token
    access_token = create_access_token(data={"sub": str(user.id)})

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }