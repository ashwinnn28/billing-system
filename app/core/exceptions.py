class BillingException(Exception):
    """Base exception for billing system."""


class ProductNotFoundException(BillingException):
    pass


class InsufficientStockException(BillingException):
    pass


class InvalidPaymentException(BillingException):
    pass