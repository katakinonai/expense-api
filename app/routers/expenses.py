from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.routers.auth import get_current_user
from app.schemas import schemas
from app.src.crud import expenses
from app.models import models

router: APIRouter = APIRouter()


@router.post("/expenses", response_model=schemas.Expense)
def create_expense(
    expense: schemas.ExpenseCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
) -> models.Expense:
    return expenses.create_expense(
        db=db, user_id=current_user.id, **expense.model_dump()
    )


@router.get("/expenses", response_model=List[schemas.Expense])
def get_expenses(
    filter_type: Optional[str] = None,
    categories: Optional[List[str]] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
) -> List[type[models.Expense]]:
    return expenses.get_expenses(
        db=db,
        user_id=current_user.id,
        filter_type=filter_type,
        categories=categories,
        start_date=start_date,
        end_date=end_date,
    )


@router.put("/expenses/{expense_id}", response_model=schemas.Expense)
def update_expense(
    expense_id: int,
    expense: schemas.ExpenseCreate,
    db: Session = Depends(get_db),
) -> models.Expense:
    db_expense: Optional[models.Expense] = expenses.update_expense(
        db=db, expense_id=expense_id, **expense.model_dump()
    )
    if db_expense is None:
        raise HTTPException(status_code=404, detail="Expense not found")
    return db_expense


@router.delete("/expenses/{expense_id}", response_model=schemas.Expense)
def delete_expense(
    expense_id: int,
    db: Session = Depends(get_db),
) -> models.Expense:
    db_expense: Optional[models.Expense] = expenses.delete_expense(
        db=db, expense_id=expense_id
    )
    if db_expense is None:
        raise HTTPException(status_code=404, detail="Expense not found")
    return db_expense
