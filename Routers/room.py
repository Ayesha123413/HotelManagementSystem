from fastapi import FastAPI,APIRouter,Depends,HTTPException,status
from supabase import create_client,Client;
from Schemas.Room import Room,RoomUpdate
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


@router.post("/delete/{room_no}",status_code=status.HTTP_200_OK)
async def delete_room(room_no:int,current_user=Depends(get_current_user)):
    existing=supabase.table("Rooms").select("*").eq("room_number",room_no).execute()
    if not existing.data:
        raise HTTPException(status_code=404, detail="room does not exist")
    result=supabase.table("Rooms").delete().eq("room_number",room_no).execute()
    if not result.data:
        raise HTTPException(status_code=500,detail="failed to delete")
    return{"message":f"Room {room_no} is succesfully deleted"}

@router.put("editRoom/{room_no}",status_code=status.HTTP_200_OK)
async def edit_room(
    room_no:int,
    room_data:RoomUpdate,
    current_user=Depends(get_current_user)):
    existing=supabase.table("Rooms").select("*").eq("room_number",room_no).execute()
    if not existing.data:
         raise HTTPException(status_code=404, detail="room does not exist")
    result=supabase.table("Rooms").update(room_data.dict()).eq("room_number",room_no).execute()
    if not result.data:
        raise HTTPException(status_code=500,detail="failed to update")
    return{"message":f"Room {room_no} is succesfully updated"}


