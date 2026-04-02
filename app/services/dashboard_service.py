from sqlalchemy.orm import Session
from sqlalchemy import func, extract

from app.db.models import FinancialRecord


def get_summary(db: Session, user_id: int):
    total_income = db.query(func.sum(FinancialRecord.amount)).filter(
        FinancialRecord.user_id == user_id,
        FinancialRecord.type == "income"
    ).scalar() or 0

    total_expense = db.query(func.sum(FinancialRecord.amount)).filter(
        FinancialRecord.user_id == user_id,
        FinancialRecord.type == "expense"
    ).scalar() or 0

    return {
        "total_income": total_income,
        "total_expense": total_expense,
        "net_balance": total_income - total_expense
    }


def get_category_breakdown(db: Session, user_id: int):
    results = db.query(
        FinancialRecord.category,
        func.sum(FinancialRecord.amount).label("total")
    ).filter(
        FinancialRecord.user_id == user_id
    ).group_by(FinancialRecord.category).all()

    return [
        {"category": r.category, "total": r.total}
        for r in results
    ]


def get_monthly_trends(db: Session, user_id: int):
    results = db.query(
        extract("month", FinancialRecord.date).label("month"),
        FinancialRecord.type,
        func.sum(FinancialRecord.amount).label("total")
    ).filter(
        FinancialRecord.user_id == user_id
    ).group_by("month", FinancialRecord.type).all()

    trends = {}

    for r in results:
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