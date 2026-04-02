from pydantic import BaseModel
from typing import List


class SummaryResponse(BaseModel):
    total_income: float
    total_expense: float
    net_balance: float


class CategoryBreakdown(BaseModel):
    category: str
    total: float


class MonthlyTrend(BaseModel):
    month: str
    income: float
    expense: float


class DashboardResponse(BaseModel):
    summary: SummaryResponse
    category_breakdown: List[CategoryBreakdown]
    monthly_trends: List[MonthlyTrend]