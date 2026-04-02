from pydantic import BaseModel
from datetime import date

class UserCreate(BaseModel):
    name: str
    email: str
    role: str


class TransactionCreate(BaseModel):
    amount: float
    type: str
    category: str
    date: date
    notes: str
    user_id: int