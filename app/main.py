from fastapi import FastAPI
from app.routers import expenses
from app.routers.auth import router as auth_router

app = FastAPI()

app.include_router(expenses.router)
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])


@app.get("/")
async def root():
    return {"message": "Welcome to Expense Tracker API!"}
