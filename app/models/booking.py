from sqlalchemy import Column, Integer, ForeignKey, Date, String
from sqlalchemy.orm import relationship

from app.db.database import Base


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    room_id = Column(Integer, ForeignKey("rooms.id"))
    guest_name = Column(String, index=True)
    check_in_date = Column(Date)
    check_out_date = Column(Date)
    guest_count = Column(Integer)
    booking_status = Column(String, default="pending")

    room = relationship("Room", back_populates="bookings")

    def __repr__(self):
        return f"<Booking {self.id} for {self.guest_name} in {self.room.hotel.name}>"