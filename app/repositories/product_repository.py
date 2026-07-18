from sqlalchemy.orm import Session

from app.models.product import Product
from app.schemas.product import ProductCreate


class ProductRepository:


    @staticmethod
    def create(
        db: Session,
        product: ProductCreate
    ):

        db_product = Product(
            **product.model_dump()
        )

        db.add(db_product)
        db.commit()
        db.refresh(db_product)

        return db_product


    @staticmethod
    def get_all(db: Session):

        return db.query(Product).all()


    @staticmethod
    def get_by_id(
        db: Session,
        product_id: int
    ):

        return (
            db.query(Product)
            .filter(Product.id == product_id)
            .first()
        )