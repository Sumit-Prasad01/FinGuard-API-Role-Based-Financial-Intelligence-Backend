from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.dependencies.auth import get_current_user
from app.services.dashboard_service import (
    get_summary,
    get_category_breakdown,
    get_monthly_trends
)
from app.schemas.dashboard import DashboardResponse

from slowapi import Limiter
from slowapi.util import get_remote_address


router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

limiter = Limiter(key_func=get_remote_address)


@router.get("/", response_model=DashboardResponse)
@limiter.limit("20/minute")   
async def get_dashboard(
    request: Request,          
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    summary = await get_summary(db, current_user.id)
    category_breakdown = await get_category_breakdown(db, current_user.id)
    monthly_trends = await get_monthly_trends(db, current_user.id)

    return {
        "summary": summary,
        "category_breakdown": category_breakdown,
        "monthly_trends": monthly_trends
    }