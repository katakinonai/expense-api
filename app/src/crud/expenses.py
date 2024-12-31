from datetime import timedelta, datetime
from typing import Optional
from app.src.crud.data_structs import Categories

from sqlalchemy.orm import Session
from app.models import models


def create_expense(
    db: Session,
    user_id: int,
    amount: float,
    category: Optional[str] = None,
    description: Optional[str] = None,
    date: Optional[datetime] = None,
) -> models.Expense:
    if not date:
        date = datetime.utcnow()
    if not category:
        category = Categories.OTHERS

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
):
    query = db.query(models.Expense).filter(models.Expense.user_id == user_id)

    if filter_type:
        match filter_type:
            case "week":
                start_date = datetime.utcnow() - timedelta(weeks=1)
            case "month":
                start_date = datetime.utcnow() - timedelta(weeks=4)
            case "year":
                start_date = datetime.utcnow() - timedelta(weeks=12)
            case _:
                start_date = None

    if not end_date:
        end_date = datetime.utcnow()

    if start_date and end_date:
        query = query.filter(
            models.Expense.date >= start_date, models.Expense.date <= end_date
        )

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
