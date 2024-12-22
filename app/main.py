import uvicorn
from fastapi import FastAPI

from app.db.database import Base, engine
from app.routers import hotel_router, room_router, user_router, booking_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(hotel_router.router)
app.include_router(room_router.router)
app.include_router(user_router.router)
app.include_router(booking_router.router)

if __name__ == '__main__':
    uvicorn.run(app)