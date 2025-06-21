from pydantic import BaseModel

class Room(BaseModel):
    room_number:int
    room_type:str
    room_status:bool
    price:int
