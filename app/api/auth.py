from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import EmailStr

from app.core.database import get_db
from app.core.auth import (
    authenticate_user,
    create_access_token,
    get_password_hash,
    get_current_user,
)
from app.models.user import User, UserRole
from app.schemas.user import UserRegister, UserLogin, TokenResponse, UserResponse

router = APIRouter(prefix="/api/auth", tags=["authentication"])


@router.post("/register", response_model=TokenResponse)
def register(user_data: UserRegister, db: Session = Depends(get_db)):
    """Register a new user account."""
    # Check if email already exists
    existing = db.query(User).filter(User.email == user_data.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Validate shelter_staff role has shelter_id
    if user_data.role == UserRole.SHELTER_STAFF and not user_data.shelter_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="shelter_id is required for shelter_staff role"
        )

    # Create new user
    new_user = User(
        email=user_data.email,
        hashed_password=get_password_hash(user_data.password),
        name=user_data.name,
        phone=user_data.phone,
        role=user_data.role,
        shelter_id=user_data.shelter_id,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Create access token
    access_token = create_access_token(data={"sub": new_user.id})

    return TokenResponse(
        access_token=access_token,
        user=UserResponse.model_validate(new_user)
    )


@router.post("/login", response_model=TokenResponse)
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    """Login with email and password."""
    user = authenticate_user(db, credentials.email, credentials.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is disabled"
        )

    # Create access token
    access_token = create_access_token(data={"sub": user.id})

    return TokenResponse(
        access_token=access_token,
        user=UserResponse.model_validate(user)
    )


@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    """Get the current authenticated user's profile."""
    return UserResponse.model_validate(current_user)


@router.post("/logout")
def logout():
    """Logout the current user (client should discard token)."""
    # With JWT, logout is handled client-side by discarding the token
    return {"message": "Successfully logged out"}
