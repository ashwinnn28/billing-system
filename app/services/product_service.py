from sqlalchemy.orm import Session

from app.repositories.product_repository import ProductRepository
from app.schemas.product import ProductCreate


class ProductService:


    @staticmethod
    def create_product(
        db: Session,
        product: ProductCreate
    ):

        return ProductRepository.create(
            db,
            product
        )


    @staticmethod
    def get_products(
        db: Session
    ):

        return ProductRepository.get_all(db)