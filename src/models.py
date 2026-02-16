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
    id: str
    is_archived: bool = False
    created_at: datetime


class CreateFeedback(BaseModel):
    email: Optional[str] = None
    text: str

class Feedback(CreateFeedback):
    id: str
    is_archived: bool=False
    created_at: datetime