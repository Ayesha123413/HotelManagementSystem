from fastapi import FastAPI,APIRouter,Depends,HTTPException,status
from supabase import create_client,Client;
from Schemas.Room import Room
from decouple import config
from auth.dependencies import get_current_user

router =APIRouter(prefix="/rooms")

url=config("SUPABASE_URL")
key=config("SUPABASE_KEY")
supabase: Client=create_client(url,key)


@router.post("/",status_code=status.HTTP_201_CREATED)
async def create_room(room:Room, current_user=Depends(get_current_user)):
    existing=supabase.table("Rooms").select("*").eq("room_number",room.room_number).execute()
    if existing.data:
        raise HTTPException(status_code=400,detail="Room already existed")
    result=supabase.table("Rooms").insert(room.dict()).execute()
    if not result.data:
        raise HTTPException(status_code=500,detail="Failed to create Room")
    return {"message":"Room is successfully created","room":result.data[0]}


