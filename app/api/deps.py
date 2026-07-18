from app.database.database import SessionLocal
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from fastapi import Depends

from app.core.security import (
    SECRET_KEY,
    ALGORITHM
)


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/login"
)


def get_current_user(
    token: str = Depends(oauth2_scheme)
):

    payload = jwt.decode(
        token,
        SECRET_KEY,
        algorithms=[ALGORITHM]
    )

    return payload

def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()