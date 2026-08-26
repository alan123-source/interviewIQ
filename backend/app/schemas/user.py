from pydantic import BaseModel,Field,EmailStr,field_validator

class UserCreate(BaseModel):
    name:str =Field(min_length=1)
    email:EmailStr
    password:str = Field(min_length=6)

    @field_validator("name")
    @classmethod
    def validate_name(cls,value):
        if not value.strip():
            raise ValueError("Name cannot be empty or contains only spaces")
        return value.strip()

class UserLogin(BaseModel):
    email:EmailStr
    password:str=Field(min_length=1)
class UserUpdate(BaseModel):
    name:str | None=Field(
        default=None,
        min_length=1
    )

    email: EmailStr | None=None
    image:str | None=Field(
        default=None,
        min_length=1
    )
    @field_validator("name")
    @classmethod
    def validate_name(cls,value):
        if not value.strip():
            raise ValueError("Name cannot be empty or contains only spaces")
        return value.strip()
    