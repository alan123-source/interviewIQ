from fastapi import Depends,HTTPException,status
from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials


from jose import jwt,JWTError
from app.core.config import JWT_SECRET
from app.utils.security import ALGORITHM
from sqlalchemy.orm import Session
from app.database.dependencies import get_db
from app.models.user import User

security=HTTPBearer()
def verify_token(token:str):
    try:
        payload=jwt.decode(
            token,
            JWT_SECRET,
            algorithms=[ALGORITHM]
        )
        return payload
    except JWTError:
        return None

def get_current_user(
    credentials:HTTPAuthorizationCredentials=Depends(security),
    db:Session=Depends(get_db)
):
    token=credentials.credentials
    payload=verify_token(token)

    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
    user_id=payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload"
        )
    user=(
        db.query(User)
        .filter(User.id==int(user_id))
        .first()
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    return user