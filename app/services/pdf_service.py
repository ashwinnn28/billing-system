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
        invoice_date = invoice_date.strftime("%d/%m/%Y, %I:%M %p").lower()

    customer = getattr(invoice, "customer", None)
    customer_name = (
        getattr(customer, "name", None)
        or f"{getattr(customer, 'first_name', '')} {getattr(customer, 'last_name', '')}".strip()
        or getattr(customer, "email", "")
        or "Customer"
    )
    customer_email = getattr(customer, "email", "")

    subtotal = getattr(invoice, "subtotal", 0) or 0
    tax = getattr(invoice, "tax", 0) or 0
    total = getattr(invoice, "total", 0) or 0
    paid_amount = getattr(invoice, "paid_amount", 0) or 0
    balance = getattr(invoice, "balance", 0) or 0
    balance_label = "Change due to customer" if balance < 0 else "Balance due from customer"
    balance_amount = abs(balance)

    def fmt(value):
        return f"Rs {value:,.2f}"

    header = [
        "Invoice receipt",
        "",
    ]

    detail_lines = [
        f"Invoice #: {invoice_number}",
        f"Date: {invoice_date}",
        "",
        f"Customer: {customer_name}",
        f"{customer_email}",
        "",
    ]

    table_header = _table_row(
        ["Product ID", "Unit Price", "Quantity", "Purchase Price", "Tax %", "Tax Value", "Total Price"],
        [16, 14, 10, 16, 8, 12, 14],
    )
    separator = "=" * 112

    rows = [table_header, separator]

    items = getattr(invoice, "invoice_items", None) or getattr(invoice, "items", None) or []
    if not items:
        rows.append("No invoice items were returned for this invoice.")
    else:
        for item in items:
            product_id = getattr(item, "product_code", None) or getattr(item, "product_id", None) or "N/A"
            quantity = getattr(item, "quantity", None) or 0
            price = getattr(item, "price", None) or getattr(item, "unit_price", None) or 0
            amount = getattr(item, "amount", None) or getattr(item, "subtotal", None) or (price * quantity)
            tax_percentage = getattr(item, "tax_percentage", None)
            tax_percentage = tax_percentage if tax_percentage is not None else getattr(item, "tax", None) or 0
            tax_amount = getattr(item, "tax_amount", None) or getattr(item, "tax_value", None) or (amount * tax_percentage / 100)
            total_price = getattr(item, "total_price", None) or getattr(item, "total", None) or (amount + tax_amount)
            rows.append(
                _table_row(
                    [
                        product_id,
                        fmt(price),
                        quantity,
                        fmt(amount),
                        f"{tax_percentage}%",
                        fmt(tax_amount),
                        fmt(total_price),
                    ],
                    [16, 14, 10, 16, 8, 12, 14],
                )
            )

    summary_lines = [
        "",
        separator,
        f"Subtotal:{fmt(subtotal):>81}",
        f"Tax:{fmt(tax):>88}",
        f"Total:{fmt(total):>86}",
        f"Paid:{fmt(paid_amount):>88}",
    ]

    return header + detail_lines + rows + summary_lines

def _table_row(columns: list[str], widths: list[int]) -> str:
    row = []
    for value, width in zip(columns, widths):
        text = str(value)
        if len(text) > width:
            text = text[: width - 3] + "..."
        row.append(text.ljust(width))
    return "  ".join(row)


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