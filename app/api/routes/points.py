from typing import List
from fastapi import APIRouter, HTTPException
from app.models.points_models import (
    AddPointRequest, 
    SpendPointsRequest, 
    SpendPointsResponse,
    SuccessResponse,
    BalanceResponse
)
from app.services.point_service import (
    add_points, 
    spend_points, 
    get_balance
)

router = APIRouter()

@router.post(
    "/add",
    response_model=SuccessResponse
)
async def add_points_endpoint(request: AddPointRequest):
    result = await add_points(request.payer, request.points, request.timestamp)
    if result is not None:
        raise HTTPException(status_code=400, detail=result)
    return SuccessResponse(message="Points added successfully")

@router.post(
    "/spend", 
    response_model=List[SpendPointsResponse]
)
async def spend_points_endpoint(request: SpendPointsRequest):
    try:
        return await spend_points(request.points)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get(
    "/balance", 
    response_model=BalanceResponse
)
async def get_balance_endpoint():
    return await get_balance()
