from pydantic import BaseModel
from datetime import datetime
from typing import Dict

class Transaction(BaseModel):
    amount: float
    reference: str
    date: datetime
    bank: str
    metadata: Dict[str, str] = {}
