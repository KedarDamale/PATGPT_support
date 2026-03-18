from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.db.engine import get_db
from src.logger.log import logger
from src.modules.auth.auth_model import User, RevokedToken
from src.modules.auth.auth_helpers import (
    hash_password, verify_password, encode_token, decode_token
)
from src.modules.auth.auth_validation_schema import (
    UserCreate, LoginRequest, UserUpdate, AdminUserUpdate
)
from src.config.env_config import settings

def register(user_create: UserCreate, db: Session):
    logger.info(f"Registering: {user_create.email}")
    if db.query(User).filter(User.email == user_create.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    user = User(
        email=user_create.email,
        hashed_password=hash_password(user_create.password),
        role=settings.DEFAULT_ROLE,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def login(user_login: LoginRequest, db: Session):
    logger.info(f"Login attempt: {user_login.email}")
    user = db.query(User).filter(User.email == user_login.email).first()
    # Avoid leaking whether email exists
    if not user or not verify_password(user_login.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if not user.is_active:
        raise HTTPException(status_code=403, detail="Account is deactivated")
    return {
        "access_token": encode_token({"sub": user.email, "role": user.role}, "access"),
        "refresh_token": encode_token({"sub": user.email}, "refresh"),
        "token_type": "bearer",
    }

def logout(refresh_token: str, db: Session):
    payload = decode_token(refresh_token)
    if payload is None or payload.get("type") != "refresh":
        raise HTTPException(status_code=400, detail="Invalid refresh token")
    jti = payload.get("jti")
    if jti and not db.query(RevokedToken).filter(RevokedToken.jti == jti).first():
        db.add(RevokedToken(jti=jti))
        db.commit()
    return {"message": "Logged out successfully"}

def refresh_tokens(refresh_token: str, db: Session):
    payload = decode_token(refresh_token)
    if payload is None or payload.get("type") != "refresh":
        raise HTTPException(status_code=400, detail="Invalid refresh token")
    jti = payload.get("jti")
    if jti and db.query(RevokedToken).filter(RevokedToken.jti == jti).first():
        raise HTTPException(status_code=401, detail="Refresh token has been revoked")
    email = payload.get("sub")
    user = db.query(User).filter(User.email == email, User.is_active == True).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found or inactive")
    # Rotate: revoke old refresh token
    if jti:
        db.add(RevokedToken(jti=jti))
        db.commit()
    return {
        "access_token": encode_token({"sub": user.email, "role": user.role}, "access"),
        "refresh_token": encode_token({"sub": user.email}, "refresh"),
        "token_type": "bearer",
    }

def get_me(current_user: User):
    return current_user

def update_me(updates: UserUpdate, current_user: User, db: Session):
    if updates.email and updates.email != current_user.email:
        if db.query(User).filter(User.email == updates.email).first():
            raise HTTPException(status_code=400, detail="Email already in use")
        current_user.email = updates.email
    if updates.password:
        current_user.hashed_password = hash_password(updates.password)
    db.commit()
    db.refresh(current_user)
    return current_user

def delete_me(current_user: User, db: Session):
    db.delete(current_user)
    db.commit()
    return {"message": "Account deleted"}

# ── Admin services ────────────────────────────────────────────────────────────

def list_users(db: Session, skip: int = 0, limit: int = 50):
    return db.query(User).offset(skip).limit(limit).all()

def admin_update_user(user_id: int, updates: AdminUserUpdate, db: Session):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if updates.role is not None:
        user.role = updates.role
    if updates.is_active is not None:
        user.is_active = updates.is_active
    db.commit()
    db.refresh(user)
    return user

def admin_delete_user(user_id: int, db: Session):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"message": f"User {user_id} deleted"}