from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.dependencies.auth import get_current_user
from app.services.dashboard_service import (
    get_summary,
    get_category_breakdown,
    get_monthly_trends
)
from app.schemas.dashboard import DashboardResponse


router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/", response_model=DashboardResponse)
async def get_dashboard(
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