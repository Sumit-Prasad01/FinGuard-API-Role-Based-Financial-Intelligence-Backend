from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from datetime import datetime

from app.db.session import get_db
from app.schemas.record import RecordCreate, RecordUpdate, RecordResponse
from app.services.record_service import (
    create_record,
    get_records,
    update_record,
    delete_record
)
from app.dependencies.auth import get_current_user

from slowapi import Limiter
from slowapi.util import get_remote_address


router = APIRouter(prefix="/records", tags=["Records"])

limiter = Limiter(key_func=get_remote_address)


@router.post("/", response_model=RecordResponse)
async def create_record_api(
    record_data: RecordCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return await create_record(db, current_user.id, record_data)


@router.get("/", response_model=List[RecordResponse])
@limiter.limit("50/minute")   
async def get_records_api(
    request: Request,          
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    category: Optional[str] = Query(None),
    type: Optional[str] = Query(None),
    search: Optional[str] = Query(None),

    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),

    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return await get_records(
        db,
        current_user.id,
        start_date,
        end_date,
        category,
        type,
        search,
        limit,
        offset
    )


@router.put("/{record_id}", response_model=RecordResponse)
async def update_record_api(
    record_id: int,
    record_data: RecordUpdate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return await update_record(db, record_id, current_user.id, record_data)


@router.delete("/{record_id}")
async def delete_record_api(
    record_id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return await delete_record(db, record_id, current_user.id)