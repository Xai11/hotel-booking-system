from datetime import date, timedelta
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from typing import List

from app.models.booking import Booking
from app.models.room import Room
from app.schemas.booking_schema import BookingInDB, BookingCreate, BookingUpdate

router = APIRouter(prefix="/bookings", tags=["Bookings"])

@router.get("/", response_model=List[BookingInDB])
def read_bookings(db: Session = Depends(get_db), guest_name: str | None = None, check_in_date: date | None = None,
                  check_out_date: date | None = None, booking_status: str | None = None):
    query = db.query(Booking)
    if guest_name:
        query = query.filter(Booking.guest_name.ilike(f"%{guest_name}%"))
    if check_in_date:
        query = query.filter(Booking.check_in_date == check_in_date)
    if check_out_date:
        query = query.filter(Booking.check_out_date == check_out_date)
    if booking_status:
        query = query.filter(Booking.booking_status == booking_status)
    return query.all()

@router.get("/{booking_id}", response_model=BookingInDB)
def read_booking(booking_id: int, db: Session = Depends(get_db)):
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return booking

@router.post("/", response_model=BookingInDB, status_code=201)
def create_booking(booking: BookingCreate, db: Session = Depends(get_db)):
    if check_availability(booking.room_id, booking.check_in_date, booking.check_out_date, db) == False:
        raise HTTPException(status_code=400, detail="The indicated dates have already been booked")
    new_booking = Booking(**booking.dict())
    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)
    return new_booking

@router.put("/{booking_id}", response_model=BookingInDB)
def update_booking(booking_id: int, booking: BookingUpdate, db: Session = Depends(get_db)):
    db_booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not db_booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    for key, value in booking.dict(exclude_unset=True).items():
        setattr(db_booking, key, value)
    db.commit()
    db.refresh(db_booking)
    return db_booking

@router.delete("/{booking_id}")
def delete_booking(booking_id: int, db: Session = Depends(get_db)):
    db_booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not db_booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    db.delete(db_booking)
    db.commit()
    return {"detail": "Booking deleted"}


def check_availability(hotel_id: int, check_in_date: date, check_out_date: date, db: Session = Depends(get_db)):
    # Проверка наличия перекрывающихся бронирований для всех дат в промежутке для всех номеров в отеле
    for i in range((check_out_date - check_in_date).days + 1):
        current_date = check_in_date + timedelta(days=i)
        overlapping_bookings = (
            db.query(Booking)
            .join(Room, Room.id == Booking.room_id)
            .filter(Room.hotel_id == hotel_id)
            .filter(
                (Booking.check_in_date <= current_date) & (Booking.check_out_date >= current_date)
            )
            .first()
        )
        if overlapping_bookings:
            return False

    return True