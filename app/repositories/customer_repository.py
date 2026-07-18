from sqlalchemy.orm import Session

from app.models.customer import Customer
from app.schemas.customer import CustomerCreate


class CustomerRepository:


    @staticmethod
    def create(
        db: Session,
        customer: CustomerCreate
    ):

        db_customer = Customer(
            **customer.model_dump()
        )

        db.add(db_customer)
        db.commit()
        db.refresh(db_customer)

        return db_customer


    @staticmethod
    def get_all(db: Session):

        return db.query(Customer).all()


    @staticmethod
    def get_by_id(
        db: Session,
        customer_id: int
    ):

        return (
            db.query(Customer)
            .filter(Customer.id == customer_id)
            .first()
        )


    @staticmethod
    def delete(
        db: Session,
        customer_id: int
    ):

        customer = (
            db.query(Customer)
            .filter(Customer.id == customer_id)
            .first()
        )

        if customer:
            db.delete(customer)
            db.commit()

        return customer