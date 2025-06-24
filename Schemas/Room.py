from pydantic import BaseModel
from typing import Optional
class Room(BaseModel):
    room_number:int
    room_type:str
    room_status:bool
    price:int
class RoomUpdate(BaseModel):
    room_type: Optional[str] = None
    room_status: Optional[bool] = None
    price: Optional[int] = None