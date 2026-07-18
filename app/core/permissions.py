from fastapi import Depends, HTTPException, status

from app.core.roles import UserRole

from app.api.deps import get_current_user



def check_role(required_role: str):

    def role_checker(
        current_user: User = Depends(get_current_user)
    ):
        if current_user.role != required_role:
            raise HTTPException(
                status_code=403,
                detail="Permission denied"
            )

        return current_user

    return role_checker


require_roles = check_role