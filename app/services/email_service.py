import logging
import os
import smtplib
from datetime import datetime
from email.message import EmailMessage

from sqlalchemy.orm import Session

from app.core.config import settings
from app.services.invoice_service import InvoiceService

logger = logging.getLogger(__name__)


def send_invoice_email(
    customer_email: str,
    invoice_id: int,
    pdf_path: str,
    db: Session
):
    try:
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"Invoice PDF not found: {pdf_path}")

        smtp_host = settings.smtp_host
        smtp_port = settings.smtp_port
        smtp_email = settings.smtp_username
        smtp_password = settings.smtp_password

        if not smtp_host or not smtp_email or not smtp_password:
            raise ValueError(
                "SMTP configuration is not complete. Verify SMTP_HOST, SMTP_PORT, SMTP_USERNAME, SMTP_PASSWORD."
            )

        invoice = InvoiceService.get_invoice(db, invoice_id)
        if invoice is None:
            raise ValueError(f"Invoice {invoice_id} not found.")

        customer = getattr(invoice, "customer", None)
        customer_name = (
            getattr(customer, "name", None)
            or f"{getattr(customer, 'first_name', '')} {getattr(customer, 'last_name', '')}".strip()
            or customer_email
        )

        invoice_ref = getattr(invoice, "invoice_number", invoice_id)
        subject = f"Your Invoice {invoice_ref} is Ready"

        body = (
            f"Hello {customer_name},\n\n"
            f"Your invoice {invoice_ref} has been generated successfully.\n"
            "Please find the attached invoice PDF.\n\n"
            "Thank you for your business.\n"
            "If you have any questions, reply to this email."
        )

        message = EmailMessage()
        message["Subject"] = subject
        message["From"] = settings.email_from
        message["To"] = customer_email
        message.set_content(body)

        with open(pdf_path, "rb") as attachment_file:
            message.add_attachment(
                attachment_file.read(),
                maintype="application",
                subtype="pdf",
                filename=os.path.basename(pdf_path)
            )

        with smtplib.SMTP(smtp_host, smtp_port, timeout=30) as smtp:
            smtp.starttls()
            smtp.login(smtp_email, smtp_password)
            smtp.send_message(message)

        InvoiceService.mark_email_sent(db, invoice_id)
        logger.info("Invoice email sent successfully for invoice %s to %s", invoice_id, customer_email)
    except Exception as e:
        logger.error(str(e))
        raise
