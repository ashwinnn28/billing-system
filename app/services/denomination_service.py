from sqlalchemy.orm import Session

from app.repositories.denomination_repository import DenominationRepository
from app.schemas.denomination import DenominationItem


class DenominationService:

    @staticmethod
    def get_denominations(db: Session):
        return DenominationRepository.get_all(db)

    @staticmethod
    def set_denominations(
        db: Session,
        items: list[DenominationItem],
    ):
        return DenominationRepository.bulk_update(db, items)

    @staticmethod
    def calculate_change(
        amount: float,
        denominations: list[DenominationItem],
    ) -> tuple[dict[int, int], float]:
        if abs(amount - round(amount)) > 1e-9:
            raise ValueError(
                "Exact change cannot be provided for fractional rupees with available denominations"
            )

        remaining = int(round(amount))
        distribution: dict[int, int] = {}
        for denom in sorted(denominations, key=lambda d: d.value, reverse=True):
            if remaining <= 0:
                break
            use_count = min(
                remaining // denom.value,
                denom.available_count,
            )
            if use_count > 0:
                distribution[denom.value] = use_count
                remaining -= denom.value * use_count

        if remaining != 0:
            raise ValueError(
                "Exact change cannot be provided with available denominations"
            )

        return distribution, amount

    @staticmethod
    def decrement_change_counts(
        db: Session,
        distribution: dict[int, int],
        commit: bool = True,
    ):
        return DenominationRepository.decrement_counts(
            db,
            distribution,
            commit=commit,
        )
