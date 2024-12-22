from pydantic import BaseModel, Field

class HotelBase(BaseModel):
    name: str = Field(..., description="Название отеля")
    address: str = Field(..., description="Адрес отеля")
    description: str = Field(..., description="Описание отеля")
    rating: float = Field(..., ge=0, le=5, description="Рейтинг отеля")

class HotelCreate(HotelBase):
    pass

class HotelUpdate(HotelBase):
    name: str | None = Field(default=None, description="Название отеля")
    address: str | None = Field(default=None, description="Адрес отеля")
    description: str | None = Field(default=None, description="Описание отеля")
    rating: float | None = Field(default=None, ge=0, le=5, description="Рейтинг отеля")

class HotelInDB(HotelBase):
    id: int = Field(..., description="Идентификатор отеля")
    number_of_rooms: int = Field(..., description="Количество номеров в отеле")

    class Config:
        orm_mode = True