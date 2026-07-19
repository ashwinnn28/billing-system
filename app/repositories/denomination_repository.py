from sqlalchemy.orm import Session

from app.models.denomination import Denomination
from app.schemas.denomination import DenominationItem


class DenominationRepository:

    @staticmethod
    def get_all(db: Session):
        return db.query(Denomination).order_by(Denomination.value.desc()).all()

    @staticmethod
    def get_by_value(db: Session, value: int):
        return (
            db.query(Denomination)
            .filter(Denomination.value == value)
            .first()
        )

    @staticmethod
    def create_or_update(
        db: Session,
        value: int,
        available_count: int,
    ):
        denomination = DenominationRepository.get_by_value(db, value)
        if denomination is None:
            denomination = Denomination(
                value=value,
                available_count=available_count,
            )
            db.add(denomination)
        else:
            denomination.available_count = available_count
        db.commit()
        db.refresh(denomination)
        return denomination

    @staticmethod
    def bulk_update(
        db: Session,
        items: list[DenominationItem],
    ):
        denominations = []
        for item in items:
            denomination = DenominationRepository.get_by_value(db, item.value)
            if denomination is None:
                denomination = Denomination(
                    value=item.value,
                    available_count=item.available_count,
                )
                db.add(denomination)
            else:
                denomination.available_count = item.available_count
            denominations.append(denomination)
        db.commit()
        for denomination in denominations:
            db.refresh(denomination)
        return denominations

    @staticmethod
    def decrement_counts(
        db: Session,
        change_distribution: dict[int, int],
        commit: bool = True,
    ):
        denominations = []
        for value, count in change_distribution.items():
            if count <= 0:
                continue
            denomination = DenominationRepository.get_by_value(db, value)
            if denomination is None:
                raise ValueError(f"Denomination {value} not found")
            if denomination.available_count < count:
                raise ValueError(
                    f"Insufficient denomination count for value {value}"
                )
            denomination.available_count -= count
            denominations.append(denomination)
        if commit:
            db.commit()
        for denomination in denominations:
            db.refresh(denomination)
        return denominations
