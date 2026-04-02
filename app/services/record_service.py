from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import Optional
from datetime import datetime

from app.db.models import FinancialRecord
from app.schemas.record import RecordCreate, RecordUpdate


def create_record(db: Session, user_id: int, record_data: RecordCreate):
    new_record = FinancialRecord(
        user_id=user_id,
        amount=record_data.amount,
        type=record_data.type,
        category=record_data.category,
        date=record_data.date,
        notes=record_data.notes,
    )

    db.add(new_record)
    db.commit()
    db.refresh(new_record)

    return new_record


def get_records(
    db: Session,
    user_id: int,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    category: Optional[str] = None,
    type: Optional[str] = None,
):
    query = db.query(FinancialRecord).filter(FinancialRecord.user_id == user_id)

    if start_date:
        query = query.filter(FinancialRecord.date >= start_date)

    if end_date:
        query = query.filter(FinancialRecord.date <= end_date)

    if category:
        query = query.filter(FinancialRecord.category == category)

    if type:
        query = query.filter(FinancialRecord.type == type)

    return query.all()


def update_record(db: Session, record_id: int, user_id: int, record_data: RecordUpdate):
    record = db.query(FinancialRecord).filter(
        FinancialRecord.id == record_id,
        FinancialRecord.user_id == user_id
    ).first()

    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Record not found"
        )

    for key, value in record_data.dict(exclude_unset=True).items():
        setattr(record, key, value)

    db.commit()
    db.refresh(record)

    return record


def delete_record(db: Session, record_id: int, user_id: int):
    record = db.query(FinancialRecord).filter(
        FinancialRecord.id == record_id,
        FinancialRecord.user_id == user_id
    ).first()

    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Record not found"
        )

    db.delete(record)
    db.commit()

    return {"message": "Record deleted successfully"}