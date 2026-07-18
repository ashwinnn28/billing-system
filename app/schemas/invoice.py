from pydantic import BaseModel
from typing import List
from datetime import datetime


class InvoiceItemCreate(BaseModel):
    product_id: str
    quantity: int


class InvoiceCreate(BaseModel):
    customer_id: int
    paid_amount: float = 0.0
    items: List[InvoiceItemCreate]


class InvoiceItemResponse(BaseModel):
    id: int
    product_id: str
    quantity: int
    price: float
    amount: float

    class Config:
        from_attributes = True


class InvoiceResponse(BaseModel):
    id: int
    invoice_number: str
    customer_id: int
    subtotal: float
    tax: float
    total: float
    paid_amount: float
    balance: float
    created_at: datetime
    items: List[InvoiceItemResponse]

    class Config:
        from_attributes = True