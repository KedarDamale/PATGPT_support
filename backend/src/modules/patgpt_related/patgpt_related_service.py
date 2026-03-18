from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from .patgpt_related_model import AboutPATGPT
from .patgpt_related_validation_schema import (
    AboutPATGPTValidationSchema,
    AboutPATGPTUpdateSchema,
)


class AboutPATGPTService:

    @staticmethod
    def create(db: Session, payload: AboutPATGPTValidationSchema) -> AboutPATGPT:
        record = AboutPATGPT(
            category=payload.category,
            data=payload.data,
            keywords=payload.keywords,
            is_active=payload.is_active,
        )
        db.add(record)
        db.commit()
        db.refresh(record)
        return record

    @staticmethod
    def get_all(
        db: Session,
        page: int,
        page_size: int,
        active_only: bool,
    ) -> dict:
        query = db.query(AboutPATGPT)
        if active_only:
            query = query.filter(AboutPATGPT.is_active == True)
        total = query.count()
        results = query.offset((page - 1) * page_size).limit(page_size).all()
        return {"total": total, "page": page, "page_size": page_size, "results": results}

    @staticmethod
    def get_by_id(db: Session, record_id: int) -> AboutPATGPT:
        record = db.query(AboutPATGPT).filter(AboutPATGPT.id == record_id).first()
        if not record:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Record with id {record_id} not found",
            )
        return record

    @staticmethod
    def update(db: Session, record_id: int, payload: AboutPATGPTUpdateSchema) -> AboutPATGPT:
        record = AboutPATGPTService.get_by_id(db, record_id)
        update_data = payload.model_dump(exclude_unset=True)  # only update provided fields
        for field, value in update_data.items():
            setattr(record, field, value)
        db.commit()
        db.refresh(record)
        return record

    @staticmethod
    def soft_delete(db: Session, record_id: int) -> AboutPATGPT:
        record = AboutPATGPTService.get_by_id(db, record_id)
        record.is_active = False
        db.commit()
        db.refresh(record)
        return record

    @staticmethod
    def hard_delete(db: Session, record_id: int) -> dict:
        record = AboutPATGPTService.get_by_id(db, record_id)
        db.delete(record)
        db.commit()
        return {"message": f"Record {record_id} permanently deleted"}