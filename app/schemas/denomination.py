from pydantic import BaseModel


class DenominationItem(BaseModel):
    value: int
    available_count: int


class DenominationResponse(BaseModel):
    value: int
    available_count: int

    class Config:
        from_attributes = True
