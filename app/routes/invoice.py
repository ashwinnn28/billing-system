from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.invoice import InvoiceCreate
from app.crud.invoice import create_invoice

from fastapi.responses import FileResponse
from app.services.pdf_service import PDFService

router = APIRouter(
    prefix="/invoices",
    tags=["Invoices"]
)


@router.post("/")
def create_new_invoice(
    invoice: InvoiceCreate,
    db: Session = Depends(get_db)
):
    try:
        return create_invoice(db, invoice)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/{invoice_id}/pdf")
def download_invoice_pdf(
    invoice_id: int,
    db: Session = Depends(get_db),
):
    file_path = PDFService.generate_invoice_pdf(
        db,
        invoice_id,
    )

    return FileResponse(
        path=file_path,
        media_type="application/pdf",
        filename=f"invoice_{invoice_id}.pdf",
    )