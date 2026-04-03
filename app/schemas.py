from pydantic import BaseModel, EmailStr
from enum import Enum
from typing import Optional
from datetime import datetime


# -----------------------------
# ROLE ENUM (only these allowed)
# -----------------------------
class UserRole(str, Enum):
    viewer = "viewer"
    analyst = "analyst"
    admin = "admin"
    manager = "manager"
    auditor = "auditor"


# -----------------------------
# USER SCHEMAS
# -----------------------------
class UserBase(BaseModel):
    name: str
    email: EmailStr
    role: UserRole


class UserCreate(UserBase):
    pass


class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True


# -----------------------------
# TRANSACTION SCHEMAS
# -----------------------------
class TransactionBase(BaseModel):
    amount: float
    category: str
    description: Optional[str] = None


class TransactionCreate(TransactionBase):
    pass


class TransactionResponse(TransactionBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# -----------------------------
# ANALYTICS RESPONSE
# -----------------------------
class SummaryResponse(BaseModel):
    total_income: float
    total_expense: float
    balance: float