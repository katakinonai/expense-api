from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.routers.auth import get_current_user
from app.schemas import schemas
from app.src.crud import expenses
from app.models import models

router: APIRouter = APIRouter()


@router.post(
    "/expenses",
    response_model=schemas.Expense,
    summary="Create a new expense",
    description="Create a new expense for the current user by providing expense details.",
    tags=["Expenses"],
)
def create_expense(
    expense: schemas.ExpenseCreate = Body(
        ...,  # Mark as required
        example={
            "amount": 100.50,
            "date": "2024-12-31T04:39:40.413Z",
            "category": "Food",
            "description": "Lunch at a restaurant",
        },
    ),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
) -> models.Expense:
    """
    Create a new expense for the logged-in user.

    Parameters:
    - expense: Expense details to create, including amount, category, date, and description.
    - db: Database session dependency.
    - current_user: The currently logged-in user (auto-injected by dependency).

    Returns:
    - The created expense record.
    """
    return expenses.create_expense(
        db=db, user_id=current_user.id, **expense.model_dump()
    )


@router.get(
    "/expenses",
    response_model=List[schemas.Expense],
    summary="Get expenses",
    description="Retrieve a list of expenses for the current user, optionally filtered by date range or type.",
    tags=["Expenses"],
)
def get_expenses(
    filter_type: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
) -> List[models.Expense]:
    """
    Get a list of expenses for the logged-in user.

    Parameters:
    - filter_type: (Optional) Filter expenses by their type (e.g., "food", "transport").
    - start_date: (Optional) Start date to filter expenses.
    - end_date: (Optional) End date to filter expenses.
    - db: Database session dependency.
    - current_user: The currently logged-in user (auto-injected by dependency).

    Returns:
    - A list of expense records matching the criteria.
    """
    return expenses.get_expenses(
        db=db,
        user_id=current_user.id,
        filter_type=filter_type,
        start_date=start_date,
        end_date=end_date,
    )


@router.put(
    "/expenses/{expense_id}",
    response_model=schemas.Expense,
    summary="Update an expense",
    description="Update an existing expense by its ID.",
    tags=["Expenses"],
)
def update_expense(
    expense_id: int,
    expense: schemas.ExpenseCreate = Body(
        ...,  # Mark as required
        example={
            "amount": 200.75,
            "date": "2024-12-31T04:39:40.413Z",
            "category": "Transportation",
            "description": "Taxi fare for business trip",
        },
    ),
    db: Session = Depends(get_db),
) -> models.Expense:
    """
    Update an existing expense by its ID.

    Parameters:
    - expense_id: ID of the expense to be updated.
    - expense: Updated expense details.
    - db: Database session dependency.

    Returns:
    - The updated expense record.

    Raises:
    - 404 HTTPException: If the expense with the given ID is not found.
    """
    db_expense: Optional[models.Expense] = expenses.update_expense(
        db=db, expense_id=expense_id, **expense.model_dump()
    )
    if db_expense is None:
        raise HTTPException(status_code=404, detail="Expense not found")
    return db_expense


@router.delete(
    "/expenses/{expense_id}",
    response_model=schemas.Expense,
    summary="Delete an expense",
    description="Delete an existing expense by its ID.",
    tags=["Expenses"],
)
def delete_expense(
    expense_id: int,
    db: Session = Depends(get_db),
) -> models.Expense:
    """
    Delete an existing expense by its ID.

    Parameters:
    - expense_id: ID of the expense to be deleted.
    - db: Database session dependency.

    Returns:
    - The deleted expense record.

    Raises:
    - 404 HTTPException: If the expense with the given ID is not found.
    """
    db_expense: Optional[models.Expense] = expenses.delete_expense(
        db=db, expense_id=expense_id
    )
    if db_expense is None:
        raise HTTPException(status_code=404, detail="Expense not found")
    return db_expense
