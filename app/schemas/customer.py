from pydantic import BaseModel, EmailStr
from datetime import datetime


class CustomerCreate(BaseModel):

    name: str
    email: EmailStr | None = None
    phone: str | None = None
    address: str | None = None


class CustomerResponse(BaseModel):

    id: int
    name: str
    email: str | None
    phone: str | None
    address: str | None
    created_at: datetime


    class Config:
        from_attributes = True