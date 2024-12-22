from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship

from app.db.database import Base


class Hotel(Base):
    __tablename__ = "hotels"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    address = Column(String, index=True)
    description = Column(String)
    rating = Column(Float)
    number_of_rooms = Column(Integer, default=0)

    rooms = relationship("Room", back_populates="hotel")

    def __repr__(self):
        return f"<Hotel {self.name}>"

