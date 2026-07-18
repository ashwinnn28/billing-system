from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate, UserLogin

from app.repositories.user_repository import UserRepository
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token
)


class AuthService:

    
    @staticmethod
    def register(
        db: Session,
        user_data: UserCreate
    ):

        existing_user = UserRepository.get_by_email(
            db,
            user_data.email
        )

        if existing_user:
            return None


        user = User(
            name=user_data.name,
            email=user_data.email,
            password=hash_password(
                user_data.password
            )
        )

        return UserRepository.create(
            db,
            user
        )


    @staticmethod
    def login(
        db: Session,
        login_data: UserLogin
    ):

        user = UserRepository.get_by_email(
            db,
            login_data.email
        )


        if not user:
            return None


        if not verify_password(
            login_data.password,
            user.password
        ):
            return None


        token = create_access_token(
            {
                "sub": str(user.id),
                "role": user.role
            }
        )


        return {
            "access_token": token,
            "token_type": "bearer"
        }
    
    @staticmethod
    def authenticate(
        db,
        email,
        password
    ):

        user = UserRepository.get_by_email(
            db,
            email
        )

        if not user:
            raise Exception("User not found")

        if not verify_password(
            password,
            user.password
        ):
            raise Exception("Invalid password")

        return user