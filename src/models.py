from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CreateCancellation(BaseModel):
    email: str
    name: str
    last_name: str
    address: str
    town: str
    town_number: str
    is_unordinary: bool = False
    reason: Optional[str] = None
    last_invoice_number: str
    termination_date: datetime

class Cancellation(CreateCancellation):
    id: int
    is_archived: bool = False
    created_at: datetime


class CreateFeedback(BaseModel):
    email: Optional[str] = None
    text: str

class Feedback(CreateFeedback):
    id: int
    is_archived: bool=False
    created_at: datetime

class User(BaseModel):
    id: str
    username: str
    email: str
    email_verified: bool = False
    is_admin: bool = False
    premium_level: int = 0
    stripe_customer_id: Optional[str] = None
    disabled: bool = False

class Token(BaseModel):
    """Token response model"""
    access_token: str
    refresh_token: Optional[str] = None
    token_type: str = "Bearer"