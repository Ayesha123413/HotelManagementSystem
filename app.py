from fastapi import FastAPI, status,HTTPException;
from decouple import config;
from supabase import create_client,Client;
import random
from Schemas.User import UserSignup,SignupResponse
from passlib.context import CryptContext
url=config("SUPABASE_URL")
key=config("SUPABASE_KEY")
jwt=config("SUPABASE_JWT_SECRET")

app=FastAPI()
supabase : Client =create_client(url,key)

pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto")

@app.post("/signup",status_code=status.HTTP_201_CREATED,tags=["Authentication"])
async def signup_user(user_data:UserSignup):
    existing_user=supabase.table("users").select("*").eq("email",user_data.email).execute()
    if existing_user.data:
        raise HTTPException(status_code=400,detail="user already existed with this email")
    result=supabase.table("user").insert({
        "name":user_data.name,
        "email":user_data.email,
        "password":pwd_context.hash(user_data.password)
    }).execute()

    if not result.data:
        raise HTTPException(status_code=500,detail="failed to create user")
    created_user=result.data[0]
    return SignupResponse(
        message="user created succesfully",
        user_id=created_user["id"],
        email=created_user["email"]
   )