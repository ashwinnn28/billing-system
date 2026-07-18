import os
from pathlib import Path
from datetime import datetime


def _escape_pdf_text(text: str) -> str:
    if text is None:
        return ""
    return str(text).replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def _build_pdf(lines: list[str]) -> bytes:
    content_lines = []
    y = 760
    for line in lines:
        content_lines.append(f"BT /F1 12 Tf 50 {y} Td ({_escape_pdf_text(line)}) Tj ET")
        y -= 18
        if y < 50:
            y = 760

    content = "\n".join(content_lines).encode("utf-8")
    stream = b"<< /Length %d >>\nstream\n%s\nendstream\n" % (len(content), content)

    obj1 = b"1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n"
    obj2 = b"2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n"
    obj3 = (
        b"3 0 obj\n"
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] "
        b"/Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >>\n"
        b"endobj\n"
    )
    obj4 = b"4 0 obj\n" + stream + b"endobj\n"
    obj5 = b"5 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>\nendobj\n"

    body = obj1 + obj2 + obj3 + obj4 + obj5
    xref_start = len(b"%PDF-1.4\n") + len(body)

    offsets = [0]
    current = len(b"%PDF-1.4\n")
    for obj in [obj1, obj2, obj3, obj4, obj5]:
        offsets.append(current)
        current += len(obj)

    xref = b"xref\n0 6\n0000000000 65535 f \n"
    for offset in offsets[1:]:
        xref += f"{offset:010d} 00000 n \n".encode("utf-8")

    trailer = (
        b"trailer\n<< /Size 6 /Root 1 0 R >>\n"
        b"startxref\n"
        + str(xref_start).encode("utf-8")
        + b"\n%%EOF\n"
    )

    return b"%PDF-1.4\n" + body + xref + trailer


def _prepare_invoice_lines(invoice) -> list[str]:
    invoice_number = getattr(invoice, "invoice_number", None) or getattr(invoice, "id", None)
    invoice_date = getattr(invoice, "date", None) or getattr(invoice, "created_at", None) or datetime.utcnow()
    if isinstance(invoice_date, datetime):
        invoice_date = invoice_date.strftime("%Y-%m-%d %H:%M:%S")

    customer = getattr(invoice, "customer", None)
    customer_name = (
        getattr(customer, "name", None)
        or f"{getattr(customer, 'first_name', '')} {getattr(customer, 'last_name', '')}".strip()
        or getattr(customer, "email", "")
        or "Customer"
    )
    customer_email = getattr(customer, "email", "")

    total_amount = getattr(invoice, "total", None) or getattr(invoice, "subtotal", None) or 0

    lines = [
        f"Invoice #{invoice_number}",
        f"Date: {invoice_date}",
        "",
        f"Customer: {customer_name}",
        f"Email: {customer_email}",
        "",
        "Items:",
    ]

    items = getattr(invoice, "invoice_items", None) or getattr(invoice, "items", None) or []
    if not items:
        lines.append("  - No items available")
    else:
        for item in items:
            description = getattr(item, "description", None) or getattr(item, "name", None) or "Item"
            quantity = getattr(item, "quantity", None) or getattr(item, "qty", None) or 1
            price = getattr(item, "price", None) or getattr(item, "unit_price", None) or 0
            line_total = getattr(item, "total", None)
            if line_total is None:
                try:
                    line_total = float(quantity) * float(price)
                except Exception:
                    line_total = price
            lines.append(f"  - {description}  Qty: {quantity}  Price: Rs {price:.2f}  Total: Rs {line_total:.2f}")

    lines.append("")
    lines.append(f"Total Amount: Rs {total_amount:.2f}")
    return lines


class PDFService:
    @staticmethod
    def generate_invoice_pdf(invoice) -> str:
        uploads_dir = Path("uploads") / "invoices"
        uploads_dir.mkdir(parents=True, exist_ok=True)

        pdf_path = uploads_dir / f"invoice_{invoice.id}.pdf"
        lines = _prepare_invoice_lines(invoice)
        pdf_bytes = _build_pdf(lines)

        with open(pdf_path, "wb") as pdf_file:
            pdf_file.write(pdf_bytes)

        return str(pdf_path)