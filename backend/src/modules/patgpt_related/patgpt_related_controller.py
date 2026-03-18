from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from src.db.engine import get_db
from src.modules.auth.auth_helpers import RoleChecker
from .patgpt_related_validation_schema import (
    AboutPATGPTValidationSchema,
    AboutPATGPTUpdateSchema,
    AboutPATGPTResponseSchema,
    PaginatedAboutPATGPTResponse,
)
from .patgpt_related_service import AboutPATGPTService

router = APIRouter(prefix="/patgpt_info", tags=["patgpt_info"])

_admin = [Depends(RoleChecker(["admin"]))]


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=AboutPATGPTResponseSchema,
    dependencies=_admin,
)
def create_patgpt_info(
    payload: AboutPATGPTValidationSchema,
    db: Session = Depends(get_db),
):
    return AboutPATGPTService.create(db, payload)


@router.get(
    "/",
    response_model=PaginatedAboutPATGPTResponse,
    dependencies=_admin,
)
def list_patgpt_info(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Items per page"),
    active_only: bool = Query(False, description="Return only active records"),
    db: Session = Depends(get_db),
):
    return AboutPATGPTService.get_all(db, page, page_size, active_only)


@router.get(
    "/{record_id}",
    response_model=AboutPATGPTResponseSchema,
    dependencies=_admin,
)
def get_patgpt_info(
    record_id: int,
    db: Session = Depends(get_db),
):
    return AboutPATGPTService.get_by_id(db, record_id)


@router.patch(
    "/{record_id}",
    response_model=AboutPATGPTResponseSchema,
    dependencies=_admin,
)
def update_patgpt_info(
    record_id: int,
    payload: AboutPATGPTUpdateSchema,
    db: Session = Depends(get_db),
):
    return AboutPATGPTService.update(db, record_id, payload)


@router.delete(
    "/{record_id}/soft",
    response_model=AboutPATGPTResponseSchema,
    dependencies=_admin,
)
def soft_delete_patgpt_info(
    record_id: int,
    db: Session = Depends(get_db),
):
    return AboutPATGPTService.soft_delete(db, record_id)


@router.delete(
    "/{record_id}",
    dependencies=_admin,
)
def hard_delete_patgpt_info(
    record_id: int,
    db: Session = Depends(get_db),
):
    return AboutPATGPTService.hard_delete(db, record_id)