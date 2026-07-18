from pydantic import BaseModel
from datetime import datetime


class ProductCreate(BaseModel):
    product_id: str
    name: str
    available_stock: int = 0
    price: float
    tax_percentage: float = 0.0


class ProductResponse(BaseModel):
    id: int
    product_id: str
    name: str
    available_stock: int
    price: float
    tax_percentage: float
    created_at: datetime

    class Config:
        from_attributes = True