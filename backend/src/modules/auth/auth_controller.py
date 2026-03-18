from fastapi import APIRouter, Depends, Query
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src.db.engine import get_db
from src.logger.log import logger
from src.modules.auth.auth_helpers import RoleChecker, get_current_user
from src.modules.auth.auth_validation_schema import (
    AdminUserUpdate, LogoutRequest, RefreshRequest,
    Token, UserCreate, UserOut, UserUpdate,
)
from src.modules.auth.auth_service import (
    admin_delete_user, admin_update_user,
    delete_me, get_me, list_users,
    login as login_service, logout,
    refresh_tokens, register as register_service,
    update_me,
)

router = APIRouter(prefix="/auth", tags=["Auth"])

# ── Public ────────────────────────────────────────────────────────────────────

@router.post("/register", response_model=UserOut, status_code=201)
def register(user_create: UserCreate, db: Session = Depends(get_db)):
    return register_service(user_create, db)

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    from src.modules.auth.auth_validation_schema import LoginRequest
    return login_service(LoginRequest(email=form_data.username, password=form_data.password), db)

@router.post("/refresh", response_model=Token)
def refresh(body: RefreshRequest, db: Session = Depends(get_db)):
    return refresh_tokens(body.refresh_token, db)

@router.post("/logout")
def logout_route(body: LogoutRequest, db: Session = Depends(get_db)):
    return logout(body.refresh_token, db)

# ── Authenticated user ────────────────────────────────────────────────────────

@router.get("/me", response_model=UserOut)
def read_me(current_user=Depends(get_current_user)):
    return get_me(current_user)

@router.patch("/me", response_model=UserOut)
def patch_me(
    updates: UserUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return update_me(updates, current_user, db)

@router.delete("/me")
def remove_me(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return delete_me(current_user, db)

# ── Admin ─────────────────────────────────────────────────────────────────────

admin_dep = Depends(RoleChecker(["admin"]))

@router.get("/users", response_model=list[UserOut], dependencies=[admin_dep])
def get_users(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=50, le=200),
    db: Session = Depends(get_db),
):
    return list_users(db, skip, limit)

@router.patch("/users/{user_id}", response_model=UserOut, dependencies=[admin_dep])
def patch_user(user_id: int, updates: AdminUserUpdate, db: Session = Depends(get_db)):
    return admin_update_user(user_id, updates, db)

@router.delete("/users/{user_id}", dependencies=[admin_dep])
def delete_user(user_id: int, db: Session = Depends(get_db)):
    return admin_delete_user(user_id, db)