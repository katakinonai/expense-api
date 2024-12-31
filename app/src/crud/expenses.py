from datetime import timedelta, datetime
from typing import Optional, List

from sqlalchemy.orm import Session
from app.models import models
from app.src.crud.data_structs import DateFilter


def create_expense(
    db: Session,
    user_id: int,
    amount: float,
    category: str,
    description: Optional[str] = None,
    date: Optional[datetime] = None,
) -> models.Expense:
    if date is None:
        date = datetime.utcnow()
    expense = models.Expense(
        user_id=user_id,
        amount=amount,
        category=category,
        description=description,
        date=date,
    )
    db.add(expense)
    db.commit()
    db.refresh(expense)
    return expense


def get_expenses(
    db: Session,
    user_id: int,
    filter_type: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    categories: Optional[List[str]] = None,
):
    query = db.query(models.Expense).filter(models.Expense.user_id == user_id)

    if filter_type:
        now = datetime.utcnow()
        match filter_type:
            case DateFilter.DAY:
                start_date = now - timedelta(days=1)
            case DateFilter.WEEK:
                start_date = now - timedelta(weeks=1)
            case DateFilter.MONTH:
                start_date = now - timedelta(weeks=4)
            case DateFilter.YEAR:
                start_date = now - timedelta(days=365)

    if start_date and end_date:
        query = query.filter(models.Expense.date.between(start_date, end_date))

    if categories:
        query = query.filter(models.Expense.category.in_(categories))

    return query.all()


def delete_expense(db: Session, expense_id: int) -> Optional[models.Expense]:
    db_expense: Optional[models.Expense] = (
        db.query(models.Expense).filter(models.Expense.id == expense_id).first()
    )
    if db_expense:
        db.delete(db_expense)
        db.commit()
    return db_expense


def update_expense(
    db: Session,
    expense_id: int,
    amount: float,
    category: str,
    description: Optional[str] = None,
    date: Optional[datetime] = None,
) -> Optional[models.Expense]:
    db_expense: Optional[models.Expense] = (
        db.query(models.Expense).filter(models.Expense.id == expense_id).first()
    )
    if db_expense:
        if date is None:
            date = db_expense.date  # type: ignore
        db_expense.amount = amount  # type: ignore
        db_expense.category = category  # type: ignore
        db_expense.description = description  # type: ignore
        db_expense.date = date  # type: ignore
        db.commit()
        db.refresh(db_expense)
    return db_expense
