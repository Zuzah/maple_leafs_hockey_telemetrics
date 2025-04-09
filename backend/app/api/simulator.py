from fastapi import APIRouter

router = APIRouter()

@router.get("/dummy")
async def dummy_metric():
    return {"message": "Simulator route placeholder"}
