from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.room import Room
from app.schemas.room_schema import RoomCreate, RoomUpdate, RoomInDB
from typing import List

router = APIRouter(prefix="/rooms", tags=["Rooms"])

@router.get("/{hotel_id}", response_model=List[RoomInDB])
def read_rooms(hotel_id: int, db: Session = Depends(get_db), room_number: int | None = None, guest_capacity: int | None = None):
    query = db.query(Room).filter(Room.hotel_id == hotel_id)
    if room_number:
        query = query.filter(Room.room_number == room_number)
    if guest_capacity:
        query = query.filter(Room.guest_capacity == guest_capacity)
    return query.all()

@router.get("/{hotel_id}/{room_id}", response_model=RoomInDB)
def read_room(hotel_id: int, room_id: int, db: Session = Depends(get_db)):
    room = db.query(Room).filter(Room.hotel_id == hotel_id, Room.id == room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    return room

@router.post("/", response_model=RoomInDB, status_code=201)
def create_room(room: RoomCreate, db: Session = Depends(get_db)):
    new_room = Room( **room.dict())
    db.add(new_room)
    db.commit()
    db.refresh(new_room)
    return new_room

@router.put("/{hotel_id}/{room_id}", response_model=RoomInDB)
def update_room(hotel_id: int, room_id: int, room: RoomUpdate, db: Session = Depends(get_db)):
    db_room = db.query(Room).filter(Room.hotel_id == hotel_id, Room.id == room_id).first()
    if not db_room:
        raise HTTPException(status_code=404, detail="Room not found")
    for key, value in room.dict(exclude_unset=True).items():
        setattr(db_room, key, value)
    db.commit()
    db.refresh(db_room)
    return db_room

@router.delete("/{hotel_id}/{room_id}")
def delete_room(hotel_id: int, room_id: int, db: Session = Depends(get_db)):
    db_room = db.query(Room).filter(Room.hotel_id == hotel_id, Room.id == room_id).first()
    if not db_room:
        raise HTTPException(status_code=404, detail="Room not found")
    db.delete(db_room)
    db.commit()
    return {"detail": "Room deleted"}