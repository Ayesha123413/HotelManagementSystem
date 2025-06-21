from fastapi import FastAPI,HTTPException,Depends,status,Header
from supabase import create_client,client
from decouple import config
import jwt


url=config("SUPABASE_URL")
key=config("SUPABSE_KEY")

supabase:client=create_client(url,key)


def get_current_user(authorization:str=Header(...)):
    try:
        if not authorization.startswith("Bearer"):
            raise ValueError("invalid token")
        token=authorization.split(" ")[1]
        user_info=supabase.auth.get_user(token)
        return user_info.user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
