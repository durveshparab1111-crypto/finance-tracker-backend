from pydantic import BaseModel
from datetime import date

class UserCreate(BaseModel):
    name: str
    email: str
    role: str
    password: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    role: str

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: str
    password: str


class TransactionCreate(BaseModel):
    amount: float
    type: str
    category: str
    date: date
    notes: str
    user_id: int