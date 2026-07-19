from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.schemas.denomination import DenominationItem, DenominationResponse
from app.services.denomination_service import DenominationService
from app.core.permissions import check_role

router = APIRouter(
    prefix="/denominations",
    tags=["Denominations"],
)


@router.get(
    "/",
    response_model=list[DenominationResponse]
)
def get_denominations(
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return DenominationService.get_denominations(db)


@router.post(
    "/",
    response_model=list[DenominationResponse]
)
def set_denominations(
    denominations: list[DenominationItem],
    db: Session = Depends(get_db),
    user=Depends(check_role(["admin", "staff"])),
):
    try:
        return DenominationService.set_denominations(db, denominations)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))
