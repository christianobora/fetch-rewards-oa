from pydantic import BaseModel, Field
from typing import Dict, List
from datetime import datetime

BalanceResponse = Dict[str, int]

class Transaction(BaseModel):
    payer: str = Field(..., example="DANNON", description="The name of the payer")
    points: int = Field(..., example=5000, description="The amount of points to be added or subtracted in the transaction")
    timestamp: datetime = Field(..., example="2020-11-02T14:00:00Z", description="The timestamp of the transaction")

    class Config:
        json_encoders = {
            datetime: lambda dt: dt.isoformat()
        }

class AddPointRequest(BaseModel):
    payer: str = Field(..., example="DANNON", description="The name of the payer")
    points: int = Field(..., example=5000, description="The amount of points to be added or subtracted in the transaction")
    timestamp: datetime = Field(..., example="2020-11-02T14:00:00Z", description="The timestamp of the transaction")

    class Config:
        json_encoders = {
            datetime: lambda dt: dt.isoformat()
        }

class SpendPointsRequest(BaseModel):
    points: int = Field(..., example=5000, description="The amount of points to be spent")

class SpendPointsResponse(BaseModel):
    payer: str = Field(..., example="DANNON", description="The name of the payer")
    points: int = Field(..., example=-5000, description="The amount of points spent")

class SuccessResponse(BaseModel):
    message: str = Field(..., example="Success", description="A message indicating the success of the operation")

class StoreData(BaseModel):
    transactions: List[Transaction] = Field(default_factory=list, description="The list of all transactions")
    balances: Dict[str, int] = Field(default_factory=dict, description="The current balance of each payer")

    class Config:
        json_encoders = {
            datetime: lambda dt: dt.isoformat()
        }