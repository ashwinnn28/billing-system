from fastapi import APIRouter

from app.api.v1.endpoints import (
    customers,
    products,
    invoices,
    payments
)


api_router = APIRouter()

api_router.include_router(
    customers.router
)

api_router.include_router(
    products.router
)

api_router.include_router(
    invoices.router
)

api_router.include_router(
    payments.router
)