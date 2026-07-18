from fastapi import Depends, HTTPException, status

from app.api.deps import get_current_user
from app.models.user import User


def check_role(required_roles: list[str] | str):

    if isinstance(required_roles, str):
        required_roles = [required_roles]

    def role_checker(
        current_user: User = Depends(get_current_user),
    ):

        if current_user.role not in required_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Permission denied",
            )

        return current_user

    return role_checker


require_roles = check_role