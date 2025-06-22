from fastapi import FastAPI,HTTPException,Depends,status,Header
from supabase import create_client,Client
from decouple import config
import jwt
from fastapi.security import HTTPAuthorizationCredentials,HTTPBearer

security=HTTPBearer()

url=config("SUPABASE_URL")
key=config("SUPABASE_KEY")

supabase:Client=create_client(url,key)


def get_current_user(credentials:HTTPAuthorizationCredentials=Header(security)):
    try:
       token=credentials.credentials
    #    print("credential:",token)
       user_info=supabase.auth.get_user(token)
       print("user Info:",user_info)

       if not user_info.user:
           raise HTTPException(
               status_code=status.HTTP_401_UNAUTHORIZED,
               detail="user not found"
           )
       return user_info.user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
