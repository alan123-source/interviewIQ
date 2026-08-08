from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.models.user import User
from app.schemas.user import UserCreate
from app.schemas.user import UserLogin
from app.utils.security import verify_password
from app.utils.security import hash_password
from app.utils.security import create_access_token
router=APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.post("/register")
def register_user(
    user:UserCreate,
    db:Session=Depends(get_db)
):
    existing_user=(
        db.query(User)
        .filter(User.email==user.email)
        .first()
    )

    if existing_user:
        return{
            "message":"Email already exists"
        }

    new_user=User(
        name=user.name,
        email=user.email,
        password=hash_password(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {
        "message":"User registered successfully"
    }
@router.post("/login")
def login_user(
    user:UserLogin,
    db:Session=Depends(get_db)
):
    existing_user=(
        db.query(User)
        .filter(User.email==user.email)
        .first()
    )

    if not existing_user:
        return{
            "message":"User not found"
        }
    if not verify_password(
        user.password,
        existing_user.password
    ):
        return{
            "message":"Invalid Password"
        }
    access_token=create_access_token(
        str(existing_user.id)
    )
    return {
        "message":"Login successfull",
        "access_token":access_token,
        "token_type":"bearer"
    }