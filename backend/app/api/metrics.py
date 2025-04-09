from fastapi import APIRouter

router = APIRouter()

@router.get("/dummy")
async def dummy_metric():
    return {"message": "Metric route placeholder"}
