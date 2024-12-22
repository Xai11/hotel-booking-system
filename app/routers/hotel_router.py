from typing import List

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.models.hotel import Hotel
from app.schemas.hotel_schema import HotelCreate, HotelInDB, HotelUpdate
from app.db.database import SessionLocal, get_db

router = APIRouter(prefix="/hotels", tags=["Hotels"])

@router.get("/", response_model=List[HotelInDB])
def read_hotels(db: Session = Depends(get_db), name: str | None = None, rating: float | None = None, address: str | None = None):
    query = db.query(Hotel)
    if name:
        query = query.filter(Hotel.name.ilike(f"%{name}%"))
    if rating:
        query = query.filter(Hotel.rating == rating)
    if address:
        query = query.filter(Hotel.address.ilike(f"%{address}%"))
    return query.all()

@router.get("/{hotel_id}", response_model=HotelInDB)
def read_hotel(hotel_id: int, db: Session = Depends(get_db)):
    hotel = db.query(Hotel).filter(Hotel.id == hotel_id).first()
    if not hotel:
        raise HTTPException(status_code=404, detail="Hotel not found")
    return hotel

@router.post("/", response_model=HotelInDB, status_code=201)
def create_hotel(hotel: HotelCreate, db: Session = Depends(get_db)):
    new_hotel = Hotel(**hotel.dict())
    db.add(new_hotel)
    db.commit()
    db.refresh(new_hotel)
    return new_hotel

@router.put("/{hotel_id}", response_model=HotelInDB)
def update_hotel(hotel_id: int, hotel: HotelUpdate, db: Session = Depends(get_db)):
    db_hotel = db.query(Hotel).filter(Hotel.id == hotel_id).first()
    if not db_hotel:
        raise HTTPException(status_code=404, detail="Hotel not found")
    for key, value in hotel.dict(exclude_unset=True).items():
        setattr(db_hotel, key, value)
    db.commit()
    db.refresh(db_hotel)
    return db_hotel

@router.delete("/{hotel_id}")
def delete_hotel(hotel_id: int, db: Session = Depends(get_db)):
    db_hotel = db.query(Hotel).filter(Hotel.id == hotel_id).first()
    if not db_hotel:
        raise HTTPException(status_code=404, detail="Hotel not found")
    db.delete(db_hotel)
    db.commit()
    return {"detail": "Hotel deleted"}

@router.post("/hotels/", response_model=HotelCreate)
def create_hotel(hotel: HotelCreate):
    db: Session = SessionLocal()
    db_hotel = Hotel(address=hotel.address)
    db.add(db_hotel)
    db.commit()
    db.refresh(db_hotel)
    db.close()
    return db_hotel
