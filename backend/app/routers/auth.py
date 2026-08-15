
from fastapi import Depends,HTTPException,status,APIRouter
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.models.user import User
from app.schemas.user import UserCreate
from app.schemas.user import UserLogin
from app.utils.security import verify_password
from app.utils.security import hash_password
from app.utils.security import create_access_token
from app.core.security import get_current_user
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
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists"
        )

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
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    if not verify_password(
        user.password,
        existing_user.password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    access_token=create_access_token(
        str(existing_user.id)
    )
    return {
        "message":"Login successfull",
        "access_token":access_token,
        "token_type":"bearer"
    }
@router.get("/profile")
def get_profile(
    current_user:User=Depends(get_current_user)

):
    return{
        "id":current_user.id,
        "name":current_user.name,
        "email":current_user.email
    }