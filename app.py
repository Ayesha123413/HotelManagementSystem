from fastapi import FastAPI, status,HTTPException;
from supabase import create_client,Client;
from decouple import config;
import random
from Schemas.User import UserSignup,SignupResponse,UserLogin,LoginResponse
from passlib.context import CryptContext



url=config("SUPABASE_URL")
key=config("SUPABASE_KEY")
# jwt=config("SUPABASE_JWT_SECRET")
app=FastAPI()

supabase : Client =create_client(url,key)

pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto")


id=random.randint(0,100)
@app.post("/signup",status_code=status.HTTP_201_CREATED,tags=["Authentication"])
async def signup_user(user_data:UserSignup):
    existing_user=supabase.table("Users").select("*").eq("email",user_data.email).execute()
    if existing_user.data:
        raise HTTPException(status_code=400,detail="user already existed with this email")
    
    auth_response= supabase.auth.sign_up({
    "email": user_data.email.strip(),
    "password":user_data.password.strip()
    })
    user_id = auth_response.user.id 
    hashed_password = pwd_context.hash(user_data.password.strip())
    result=supabase.table("Users").insert({
        "id":user_id,
        "name":user_data.name,
        "email": user_data.email.strip(),
        "password":hashed_password
    }).execute()

    if not result.data:
        raise HTTPException(status_code=500,detail="failed to create user")
    created_user=result.data[0]
    return SignupResponse(
        message="user created succesfully",
        user_id=created_user["id"],
        email=user_data.email
   )


@app.post("/login",response_model=LoginResponse)
async def login_user(credentials:UserLogin):
    result=supabase.table("Users").select("*").eq("email",credentials.email).single().execute()
    if result.data is None:
        raise HTTPException(status_code=401,detail="Invalid email or password")
    user=result.data
    # hashed_password=user["password"]
    print("result",result,credentials.password,user["password"])
    try:
        auth_response = supabase.auth.sign_in_with_password({
            "email": credentials.email,
            "password": credentials.password
        })
    except Exception as e:
        if "Email not confirmed" in str(e):
            raise HTTPException(status_code=403, detail="Please confirm your email before logging in.")
        raise HTTPException(status_code=401, detail="Authentication failed.")

    print("auth respinse",auth_response)
    session=auth_response.session
    user=auth_response.user
    return LoginResponse(
        message="login sucessful",
        access_token=session.access_token,
        refresh_token=session.refresh_token,
        token_type="bearer",
        user_id=user.id,
        email=user.email


    )
