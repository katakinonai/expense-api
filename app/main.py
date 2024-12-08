from fastapi import FastAPI, Depends

from app.db.database import init_db
from app.models.models import User
from app.routers import expenses
from app.routers.auth import router as auth_router, get_current_user

app = FastAPI()

app.include_router(expenses.router)
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])


@app.get("/")
async def root():
    return {"message": "Welcome to Expense Tracker API!"}


@app.get("/protected")
def protected_route(current_user: User = Depends(get_current_user)):
    return {"message": f"Hello, {current_user.username}!"}


init_db()
