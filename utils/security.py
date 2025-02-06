import hashlib

from fastapi import HTTPException, Request
from jose import JWTError, jwt
from passlib.context import CryptContext

from configs.config import config


class token_context:
    secret_key = config.SECRET_KEY
    algorithm = "HS256"


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    password_bytes = password.encode("utf-8")
    sha256_hash = hashlib.sha256()
    sha256_hash.update(password_bytes)
    hashed_password = sha256_hash.hexdigest()
    return hashed_password


def compare_passwords(plain_text_password: str, hashed_password: str) -> bool:
    hashed_plain_text_password = hash_password(plain_text_password)
    return hashed_plain_text_password == hashed_password


def create_access_token(data: dict):
    to_encode = data.copy()
    return jwt.encode(
        to_encode, token_context.secret_key, algorithm=token_context.algorithm
    )


async def decode_access_token(request: Request) -> str:
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    try:
        payload = jwt.decode(
            token, token_context.secret_key, algorithms=[token_context.algorithm]
        )
        email: str = payload.get("email")
        if email is None:
            raise HTTPException(status_code=401, detail="Not authenticated")
        else:
            return email
    except JWTError:
        raise HTTPException(status_code=401, detail="Not authenticated")
