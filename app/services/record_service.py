from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from typing import Optional
from datetime import datetime

from app.db.models import FinancialRecord
from app.schemas.record import RecordCreate, RecordUpdate


async def create_record(db: AsyncSession, user_id: int, record_data: RecordCreate):
    new_record = FinancialRecord(
        user_id=user_id,
        amount=record_data.amount,
        type=record_data.type,
        category=record_data.category,
        date=record_data.date,
        notes=record_data.notes,
    )

    db.add(new_record)
    await db.commit()
    await db.refresh(new_record)

    return new_record



async def get_records(
    db: AsyncSession,
    user_id: int,
    start_date=None,
    end_date=None,
    category=None,
    type=None,
    search=None,
    limit: int = 10,
    offset: int = 0,
):
    query = select(FinancialRecord).where(FinancialRecord.user_id == user_id)

    if start_date:
        query = query.where(FinancialRecord.date >= start_date)

    if end_date:
        query = query.where(FinancialRecord.date <= end_date)

    if category:
        query = query.where(FinancialRecord.category == category)

    if type:
        query = query.where(FinancialRecord.type == type)

    if search:
        query = query.where(
            or_(
                FinancialRecord.category.ilike(f"%{search}%"),
                FinancialRecord.notes.ilike(f"%{search}%")
            )
        )

    query = query.limit(limit).offset(offset)

    result = await db.execute(query)
    return result.scalars().all()


async def update_record(
    db: AsyncSession,
    record_id: int,
    user_id: int,
    record_data: RecordUpdate
):
    result = await db.execute(
        select(FinancialRecord).where(
            FinancialRecord.id == record_id,
            FinancialRecord.user_id == user_id
        )
    )
    record = result.scalar_one_or_none()

    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Record not found"
        )

    for key, value in record_data.model_dump(exclude_unset=True).items():
        setattr(record, key, value)

    await db.commit()
    await db.refresh(record)

    return record


async def delete_record(db: AsyncSession, record_id: int, user_id: int):
    result = await db.execute(
        select(FinancialRecord).where(
            FinancialRecord.id == record_id,
            FinancialRecord.user_id == user_id
        )
    )
    record = result.scalar_one_or_none()

    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Record not found"
        )

    await db.delete(record)
    await db.commit()

    return {"message": "Record deleted successfully"}