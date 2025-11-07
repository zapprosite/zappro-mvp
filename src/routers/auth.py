from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from src.database import get_db
from src.models.user import User as UserModel
from src.schemas.auth import (
    RefreshRequest,
    RefreshResponse,
    Token,
    User,
    UserCreate,
    UserLogin,
)
from src.utils.auth import (
    create_access_token,
    generate_refresh_token,
    get_password_hash,
    verify_password,
    verify_refresh_token,
)

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])
optional_bearer = HTTPBearer(auto_error=False)


@router.post("/register", response_model=User, status_code=status.HTTP_201_CREATED)
def register(user: UserCreate, db: Session = Depends(get_db)) -> User:
    # Check if user already exists
    existing = db.query(UserModel).filter(UserModel.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = get_password_hash(user.password)
    db_user = UserModel(
        email=user.email,
        name=user.name,
        role=user.role,
        hashed_password=hashed_password,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user  # type: ignore[return-value]


@router.post("/login", response_model=Token)
def login(user_credentials: UserLogin, db: Session = Depends(get_db)) -> Token:
    user = db.query(UserModel).filter(UserModel.email == user_credentials.email).first()
    if not user or not verify_password(user_credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    access_token = create_access_token(data={"sub": user.email})
    refresh_token = generate_refresh_token(data={"sub": user.email})
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "user": user,  # type: ignore[dict-item]
    }


@router.post("/refresh", response_model=RefreshResponse)
def refresh_token_endpoint(
    payload: RefreshRequest | None = None,
    credentials: HTTPAuthorizationCredentials | None = Depends(optional_bearer),
    db: Session = Depends(get_db),
) -> RefreshResponse:
    token = (payload.refresh_token if payload else None) or (
        credentials.credentials if credentials else None
    )
    if not token:
        raise HTTPException(status_code=400, detail="Refresh token required")

    decoded = verify_refresh_token(token)
    email = decoded.get("sub")
    if not email:
        raise HTTPException(status_code=401, detail="Invalid refresh token subject")

    user = db.query(UserModel).filter(UserModel.email == email).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    access_token = create_access_token({"sub": user.email})
    return RefreshResponse(access_token=access_token)
