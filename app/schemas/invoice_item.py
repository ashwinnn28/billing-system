from pydantic import BaseModel


class InvoiceItemCreate(BaseModel):

    invoice_id: int
    product_id: int
    quantity: int
    price: float



class InvoiceItemResponse(BaseModel):

    id: int
    invoice_id: int
    product_id: int
    quantity: int
    price: float


    class Config:
        from_attributes = True