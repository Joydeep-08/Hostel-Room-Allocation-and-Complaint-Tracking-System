"""Pydantic request/response contracts shared by API clients and services."""
from datetime import date
from decimal import Decimal
from pydantic import BaseModel, ConfigDict, Field

class APIModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

class UserCreate(BaseModel):
    full_name: str = Field(min_length=1, max_length=120)
    email: str
    password: str = Field(min_length=8)
    role: str = "resident"

class UserRead(APIModel):
    id: int
    full_name: str
    email: str
    role: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class AllocationCreate(BaseModel):
    resident_id: int
    bed_id: int
    start_date: date

class TransferCreate(BaseModel):
    destination_bed_id: int
    reason: str = Field(min_length=1, max_length=500)

class PaymentCreate(BaseModel):
    amount: Decimal = Field(gt=0)
    payment_reference: str = Field(min_length=1, max_length=80)
