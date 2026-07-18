from datetime import datetime, timedelta

from jose import jwt
from passlib.context import CryptContext


SECRET_KEY = "billing-secret-key"
ALGORITHM = "HS256"


pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


def hash_password(password: str):
    password = password.encode("utf-8")[:72]
    password = password.decode("utf-8", "ignore")

    return pwd_context.hash(password)



def verify_password(
    plain_password,
    hashed_password
):

    plain_password = plain_password.encode("utf-8")[:72]
    plain_password = plain_password.decode("utf-8", "ignore")

    return pwd_context.verify(
        plain_password,
        hashed_password
    )


def create_access_token(
    data: dict
):

    token_data = data.copy()

    expire = datetime.utcnow() + timedelta(
        minutes=60
    )

    token_data.update(
        {
            "exp": expire
        }
    )

    return jwt.encode(
        token_data,
        SECRET_KEY,
        algorithm=ALGORITHM
    )