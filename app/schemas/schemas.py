from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        from_attributes = True


class ExpenseBase(BaseModel):
    amount: float
    category: str
    description: Optional[str] = None
    date: Optional[datetime] = None


class ExpenseCreate(BaseModel):
    amount: float
    date: Optional[datetime] = None
    category: Optional[str] = None
    description: Optional[str] = None


class Expense(ExpenseBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True
