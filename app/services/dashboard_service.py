from sqlalchemy import func, extract, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import FinancialRecord


async def get_summary(db: AsyncSession, user_id: int):
    income_result = await db.execute(
        select(func.sum(FinancialRecord.amount)).where(
            FinancialRecord.user_id == user_id,
            FinancialRecord.type == "income"
        )
    )
    total_income = income_result.scalar() or 0

    expense_result = await db.execute(
        select(func.sum(FinancialRecord.amount)).where(
            FinancialRecord.user_id == user_id,
            FinancialRecord.type == "expense"
        )
    )
    total_expense = expense_result.scalar() or 0

    return {
        "total_income": total_income,
        "total_expense": total_expense,
        "net_balance": total_income - total_expense
    }


async def get_category_breakdown(db: AsyncSession, user_id: int):
    result = await db.execute(
        select(
            FinancialRecord.category,
            func.sum(FinancialRecord.amount).label("total")
        )
        .where(FinancialRecord.user_id == user_id)
        .group_by(FinancialRecord.category)
    )

    rows = result.all()

    return [
        {"category": r.category, "total": r.total}
        for r in rows
    ]


async def get_monthly_trends(db: AsyncSession, user_id: int):
    result = await db.execute(
        select(
            extract("month", FinancialRecord.date).label("month"),
            FinancialRecord.type,
            func.sum(FinancialRecord.amount).label("total")
        )
        .where(FinancialRecord.user_id == user_id)
        .group_by("month", FinancialRecord.type)
    )

    rows = result.all()

    trends = {}

    for r in rows:
        month = int(r.month)
        if month not in trends:
            trends[month] = {"income": 0, "expense": 0}

        trends[month][r.type] = r.total

    return [
        {
            "month": str(month),
            "income": data["income"],
            "expense": data["expense"]
        }
        for month, data in sorted(trends.items())
    ]