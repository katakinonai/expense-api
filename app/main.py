from fastapi import FastAPI
from app.routers import expenses

app = FastAPI()

app.include_router(expenses.router)


@app.get("/")
async def root():
    return {"message": "Welcome to Expense Tracker API!"}
