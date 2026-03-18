from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session
from src.db.engine import get_db
from src.modules.auth.auth_helpers import RoleChecker, get_current_user
from .memory_model import UserMemory
from .memory_store import MemoryStore
from .memory_validation_schema import (
    UserMemoryResponseSchema,
    UserMemoryUpdateSchema,
    PaginatedMemoryResponse,
)

router = APIRouter(prefix="/memories", tags=["memories"])

_admin = [Depends(RoleChecker(["admin"]))]
_user  = [Depends(RoleChecker(["user", "admin"]))]


# ═══════════════════════════════════════════════════════════════
# USER ROUTES — own memories only
# ═══════════════════════════════════════════════════════════════

@router.get("/my", response_model=list[UserMemoryResponseSchema], dependencies=_user,
            summary="Get all my remembered memories")
def get_my_memories(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return db.query(UserMemory).filter_by(user_id=current_user.id).all()


@router.delete("/my/{key}", dependencies=_user,
               summary="Delete one of my memories by key")
def delete_my_memory(
    key: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    deleted = MemoryStore.delete(db, current_user.id, key)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No memory found for key '{key}'")
    return {"message": f"Forgot '{key}'"}


@router.delete("/my", dependencies=_user,
               summary="Wipe all my memories")
def delete_all_my_memories(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    db.query(UserMemory).filter_by(user_id=current_user.id).delete()
    db.commit()
    MemoryStore.invalidate_user(current_user.id)   # flush RAM cache too
    return {"message": "All your memories have been wiped"}


# ═══════════════════════════════════════════════════════════════
# ADMIN ROUTES — any user's memories
# ═══════════════════════════════════════════════════════════════

@router.get("/admin/all", response_model=PaginatedMemoryResponse, dependencies=_admin,
            summary="[Admin] All memories across all users")
def admin_get_all_memories(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    user_id: int | None = Query(None, description="Filter by a specific user"),
    db: Session = Depends(get_db),
):
    query = db.query(UserMemory)
    if user_id:
        query = query.filter(UserMemory.user_id == user_id)
    total = query.count()
    results = (query.order_by(UserMemory.user_id, UserMemory.key)
                    .offset((page - 1) * page_size)
                    .limit(page_size)
                    .all())
    return {"total": total, "page": page, "page_size": page_size, "results": results}


@router.get("/admin/user/{user_id}", response_model=list[UserMemoryResponseSchema],
            dependencies=_admin, summary="[Admin] All memories for a specific user")
def admin_get_user_memories(
    user_id: int,
    db: Session = Depends(get_db),
):
    return db.query(UserMemory).filter_by(user_id=user_id).all()


@router.patch("/admin/user/{user_id}/{key}", response_model=UserMemoryResponseSchema,
              dependencies=_admin, summary="[Admin] Edit a specific memory value")
def admin_update_memory(
    user_id: int,
    key: str,
    payload: UserMemoryUpdateSchema,
    db: Session = Depends(get_db),
):
    memory = db.query(UserMemory).filter_by(user_id=user_id, key=key).first()
    if not memory:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No memory '{key}' for user {user_id}")
    memory.value = payload.value
    db.commit()
    db.refresh(memory)
    MemoryStore.invalidate_user(user_id)   # force re-warm from DB on next access
    return memory


@router.delete("/admin/user/{user_id}/{key}", dependencies=_admin,
               summary="[Admin] Delete a specific memory for a user")
def admin_delete_memory(
    user_id: int,
    key: str,
    db: Session = Depends(get_db),
):
    deleted = MemoryStore.delete(db, user_id, key)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No memory '{key}' for user {user_id}")
    return {"message": f"Deleted memory '{key}' for user {user_id}"}


@router.delete("/admin/user/{user_id}", dependencies=_admin,
               summary="[Admin] Wipe all memories for a user")
def admin_wipe_user_memories(
    user_id: int,
    db: Session = Depends(get_db),
):
    db.query(UserMemory).filter_by(user_id=user_id).delete()
    db.commit()
    MemoryStore.invalidate_user(user_id)
    return {"message": f"All memories wiped for user {user_id}"}