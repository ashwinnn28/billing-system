import os

from reportlab.pdfgen import canvas
from sqlalchemy.orm import Session

from app.models.customer import Customer
from app.models.invoice import Invoice
from app.models.invoice_item import InvoiceItem
from app.models.product import Product


class PDFService:
    """
    Service for generating Invoice PDFs.
    """

    OUTPUT_DIR = "generated_invoices"

    @classmethod
    def generate_invoice_pdf(
        cls,
        db: Session,
        invoice_id: int,
    ) -> str:
        """
        Generate invoice PDF and return file path.
        """

        invoice = (
            db.query(Invoice)
            .filter(Invoice.id == invoice_id)
            .first()
        )

        if not invoice:
            raise ValueError("Invoice not found")

        customer = (
            db.query(Customer)
            .filter(Customer.id == invoice.customer_id)
            .first()
        )

        items = (
            db.query(InvoiceItem)
            .filter(InvoiceItem.invoice_id == invoice.id)
            .all()
        )

        os.makedirs(cls.OUTPUT_DIR, exist_ok=True)

        file_path = os.path.join(
            cls.OUTPUT_DIR,
            f"{invoice.invoice_number}.pdf",
        )

        pdf = canvas.Canvas(file_path)

        cls._header(pdf, invoice)

        cls._customer_section(
            pdf,
            customer,
        )

        cls._items_table(
            pdf,
            db,
            items,
        )

        cls._summary(
            pdf,
            invoice,
        )

        cls._footer(pdf)

        pdf.save()

        return file_path

    @staticmethod
    def _header(
        pdf,
        invoice,
    ):

        pdf.setFont("Helvetica-Bold", 18)
        pdf.drawString(220, 800, "INVOICE")

        pdf.setFont("Helvetica", 12)

        pdf.drawString(
            50,
            760,
            f"Invoice No : {invoice.invoice_number}",
        )

        pdf.drawString(
            50,
            740,
            f"Date : {invoice.created_at.strftime('%d-%b-%Y')}",
        )

    @staticmethod
    def _customer_section(
        pdf,
        customer,
    ):

        pdf.setFont("Helvetica-Bold", 14)
        pdf.drawString(50, 700, "Customer")

        pdf.setFont("Helvetica", 12)

        pdf.drawString(
            50,
            675,
            f"Name : {customer.name}",
        )

        pdf.drawString(
            50,
            655,
            f"Email : {customer.email or '-'}",
        )

        pdf.drawString(
            50,
            635,
            f"Phone : {customer.phone or '-'}",
        )

        pdf.drawString(
            50,
            615,
            f"Address : {customer.address or '-'}",
        )

    @staticmethod
    def _items_table(
        pdf,
        db: Session,
        items,
    ):

        y = 570

        pdf.setFont("Helvetica-Bold", 12)

        pdf.drawString(50, y, "Product")
        pdf.drawString(250, y, "Qty")
        pdf.drawString(330, y, "Price")
        pdf.drawString(450, y, "Amount")

        y -= 20

        pdf.line(50, y + 10, 550, y + 10)

        pdf.setFont("Helvetica", 11)

        for item in items:

            product = (
                db.query(Product)
                .filter(Product.id == item.product_id)
                .first()
            )

            pdf.drawString(
                50,
                y,
                product.name,
            )

            pdf.drawString(
                250,
                y,
                str(item.quantity),
            )

            pdf.drawString(
                330,
                y,
                f"{item.unit_price:.2f}",
            )

            pdf.drawString(
                450,
                y,
                f"{item.subtotal:.2f}",
            )

            y -= 20

    @staticmethod
    def _summary(
        pdf,
        invoice,
    ):

        y = 250

        pdf.line(300, y + 100, 550, y + 100)

        pdf.setFont("Helvetica-Bold", 12)

        pdf.drawString(
            320,
            y + 75,
            f"Subtotal : {invoice.subtotal:.2f}",
        )

        pdf.drawString(
            320,
            y + 55,
            f"GST (18%) : {invoice.tax:.2f}",
        )

        pdf.drawString(
            320,
            y + 35,
            f"Total : {invoice.total:.2f}",
        )

        pdf.drawString(
            320,
            y + 15,
            f"Paid : {invoice.paid_amount:.2f}",
        )

        pdf.drawString(
            320,
            y - 5,
            f"Balance : {invoice.balance:.2f}",
        )

    @staticmethod
    def _footer(
        pdf,
    ):

        pdf.setFont("Helvetica-Oblique", 12)

        pdf.drawString(
            150,
            80,
            "Thank you for your purchase.",
        )