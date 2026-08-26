
from fastapi import Depends,HTTPException,status,APIRouter
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.models.user import User
from app.schemas.user import UserCreate
from app.schemas.user import UserLogin
from app.schemas.user import UserUpdate
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
        password_hash=hash_password(user.password)
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
        existing_user.password_hash
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

@router.put("/profile")
def update_profile(
    user_data:UserUpdate,
    current_user:User=Depends(get_current_user),
    db:Session=Depends(get_db)
):
    if (
        user_data.name is None
        and user_data.email is None
        and user_data.image is None
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="At least one field must be provided"
        )
    if user_data.name is not None:
        current_user.name=user_data.name
    if user_data.email is not None:
        
        existing_user=(
            
            db.query(User)
            .filter(
                User.email==user_data.email,
                User.id!=current_user.id
            )
            .first()
        )
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already exists"
            )
        current_user.email=user_data.email
    if user_data.image is not None:
        current_user.image=user_data.image
    db.commit()
    db.refresh(current_user)

    return {
        "message":"Profile updated successfully",
        "user":{
            "id":current_user.id,
            "name":current_user.name,
            "email":current_user.email,
            "image":current_user.image
        }
    }

@router.get("/users/{user_id}")
def get_user(
    user_id:int,
    current_user:User=Depends(get_current_user),
    db:Session=Depends(get_db)
):
    if user_id!=current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to access this user"
        )

    user=(
        db.query(User)
        .filter(User.id==user_id)
        .first()
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return {
        "id":user.id,
        "name":user.name,
        "email":user.email
    }