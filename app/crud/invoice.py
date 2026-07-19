from datetime import datetime

from sqlalchemy.orm import Session, joinedload

from app.models.customer import Customer
from app.models.product import Product
from app.models.invoice import Invoice
from app.models.invoice_item import InvoiceItem
from app.services.denomination_service import DenominationService

GST_PERCENTAGE = 18.0


def create_invoice(db: Session, invoice_data):
    """
    Create a new invoice.
    """

    # Check customer
    customer = (
        db.query(Customer)
        .filter(Customer.id == invoice_data.customer_id)
        .first()
    )

    if not customer:
        raise ValueError("Customer not found")

    subtotal = 0.0
    invoice_items = []

    # Validate products
    for item in invoice_data.items:

        product = (
            db.query(Product)
            .filter(Product.product_id == item.product_id)
            .first()
        )

        if not product:
            raise ValueError(f"Product {item.product_id} not found")

        if product.available_stock < item.quantity:
            raise ValueError(
                f"Insufficient stock for {product.name}"
            )

        amount = product.price * item.quantity

        subtotal += amount

        invoice_items.append(
            {
                "product": product,
                "quantity": item.quantity,
                "price": product.price,
                "amount": amount,
            }
        )

    # Calculate totals
    tax = subtotal * (GST_PERCENTAGE / 100)
    total = subtotal + tax

    # Payment calculation
    paid_amount = invoice_data.paid_amount

    if paid_amount < 0:
        raise ValueError("Paid amount cannot be negative")

    if invoice_data.denominations:
        DenominationService.set_denominations(db, invoice_data.denominations)

    balance = total - paid_amount

    # Create invoice
    invoice = Invoice(
        invoice_number=f"INV-{int(datetime.utcnow().timestamp())}",
        customer_id=invoice_data.customer_id,
        subtotal=subtotal,
        tax=tax,
        total=total,
        paid_amount=paid_amount,
        balance=balance,
    )

    db.add(invoice)

    # Generate invoice ID
    db.flush()

    # Create invoice items
    for item in invoice_items:

        invoice_item = InvoiceItem(
            invoice_id=invoice.id,
            product_id=item["product"].id,
            quantity=item["quantity"],
            unit_price=item["product"].price,
            tax_percentage=item["product"].tax_percentage,
            subtotal=item["product"].price * item["quantity"],
        )

        db.add(invoice_item)

        # Update stock
        item["product"].available_stock -= item["quantity"]

    change_distribution = None
    try:
        if paid_amount > total:
            change_amount = paid_amount - total
            if round(change_amount, 2) != int(change_amount):
                raise ValueError(
                    "Change cannot be provided for fractional rupees with available denominations"
                )

            denominations = DenominationService.get_denominations(db)
            distribution, _ = DenominationService.calculate_change(
                change_amount,
                denominations,
            )
            DenominationService.decrement_change_counts(
                db,
                distribution,
                commit=False,
            )
            change_distribution = distribution

        db.commit()
        db.refresh(invoice)
    except Exception:
        db.rollback()
        raise

    if change_distribution is not None:
        invoice.change_distribution = change_distribution

    return invoice


def get_invoice(db: Session, invoice_id: int):

    return (
        db.query(Invoice)
        .filter(Invoice.id == invoice_id)
        .first()
    )


def get_invoices(db: Session):

    return (
        db.query(Invoice)
        .order_by(Invoice.id.desc())
        .all()
    )


def get_invoices_by_customer(
    db: Session,
    customer_id: int
):
    return (
        db.query(Invoice)
        .filter(Invoice.customer_id == customer_id)
        .order_by(Invoice.id.desc())
        .all()
    )


def get_invoice_with_items(
    db: Session,
    invoice_id: int
):
    return (
        db.query(Invoice)
        .options(
            joinedload(Invoice.customer),
            joinedload(Invoice.invoice_items).joinedload(
                InvoiceItem.product
            )
        )
        .filter(Invoice.id == invoice_id)
        .first()
    )