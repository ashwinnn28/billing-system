from fastapi import APIRouter, Depends

from app.core.permissions import check_role
from app.core.roles import UserRole


router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)


@router.get("/users")
def get_users(
    current_user = Depends(
        check_role(UserRole.ADMIN)
    )
):

    return {
        "message":
        "Admin access granted"
    }