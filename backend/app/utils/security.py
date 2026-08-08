from passlib.context import CryptContext
from datetime import datetime,timedelta,timezone

from jose import jwt

from app.core.config import JWT_SECRET

pwd_context=CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

def hash_password(password:str):
    return pwd_context.hash(password)

def verify_password(
    plain_password:str,
    hashed_password:str
):
    return pwd_context.verify(
        plain_password,
        hashed_password
    )

ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30

def create_access_token(user_id:str):
    expire=datetime.now(timezone.utc)+timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )
    payload={
        "sub":user_id,
        "exp":expire,
    }

    return jwt.encode(
        payload,
        JWT_SECRET,
        algorithm=ALGORITHM
    )