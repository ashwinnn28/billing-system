from pydantic import BaseModel
from datetime import datetime


class InvoiceCreate(BaseModel):

    customer_id: int



class InvoiceResponse(BaseModel):

    id: int
    customer_id: int
    total_amount: float
    status: str
    created_at: datetime


    class Config:
        from_attributes = True