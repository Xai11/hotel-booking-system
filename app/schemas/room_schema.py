from pydantic import BaseModel, Field


class RoomBase(BaseModel):
    hotel_id: int = Field(..., description="Идентификатор отеля")
    room_number: int = Field(..., description="Номер в отеле")
    description: str = Field(..., description="Описание номера")
    guest_capacity: int = Field(..., description="Количество гостей в номере")

class RoomCreate(RoomBase):
    pass

class RoomUpdate(RoomBase):
    hotel_id: int | None = Field(default=None, description="Идентификатор отеля")
    room_number: int | None = Field(default=None, description="Номер в отеле")
    description: str | None = Field(default=None, description="Описание номера")
    guest_capacity: int | None = Field(default=None, description="Количество гостей в номере")

class RoomInDB(RoomBase):
    id: int = Field(..., description="Идентификатор номера")

    class Config:
        orm_mode = True