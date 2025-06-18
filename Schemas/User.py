
from pydantic import BaseModel,EmailStr;
from typing import Optional;

class UserSignup(BaseModel):
    name:str
    email:EmailStr
    password:str

class UserLogin(BaseModel):
    email:EmailStr
    password:str
    
class SignupResponse(BaseModel):
    message:str
    user_id:int
    email:EmailStr
class LoginResponse(BaseModel):
    message:str
    access_token:str
    refresh_token:str
    token_type:str="bearer"
    user_id:int
    email:EmailStr