from pydantic import BaseModel,Field

class UserCreate(BaseModel):
    name:str =Field(min_length=1)
    email:str = Field(min_length=1)
    password:str = Field(min_length=6)
class UserLogin(BaseModel):
    email:str=Field(min_length=1)
    password:str=Field(min_length=1)