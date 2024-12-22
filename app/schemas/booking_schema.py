from pydantic import BaseModel, Field
from datetime import date


class BookingBase(BaseModel):
    room_id: int = Field(..., description="Идентификатор номера")
    guest_name: str = Field(..., description="Имя гостя")
    check_in_date: date = Field(..., description="Дата заезда")
    check_out_date: date = Field(..., description="Дата выезда")
    guest_count: int = Field(..., description="Количество гостей")
    booking_status: str = Field(..., description="Статус бронирования")

class BookingCreate(BookingBase):
    pass

class BookingUpdate(BookingBase):
    room_id: int | None = Field(default=None, description="Идентификатор номера")
    guest_name: str | None = Field(default=None, description="Имя гостя")
    check_in_date: date | None = Field(default=None, description="Дата заезда")
    check_out_date: date | None = Field(default=None, description="Дата выезда")
    guest_count: int | None = Field(default=None, description="Количество гостей")
    booking_status: str | None = Field(default=None, description="Статус бронирования")

class BookingInDB(BookingBase):
    id: int = Field(..., description="Идентификатор бронирования")

    class Config:
        orm_mode = True