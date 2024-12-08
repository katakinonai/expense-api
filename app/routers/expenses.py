from typing import Dict, List

from fastapi import APIRouter

router: APIRouter = APIRouter()


@router.get("/expenses")
async def get_expenses() -> Dict[str, List]:
    return {"expenses": []}
