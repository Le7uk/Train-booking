from pydantic import BaseModel
from datetime import datetime
from .route import RouteResponse


class BookingCreate(BaseModel):
    route_id: int
    seat_number: int

class BookingResponse(BaseModel):
    id: int
    user_id: int
    route_id: int
    seat_number: int
    booking_date: datetime
    status: str
    route: RouteResponse
    
    class Config:
        from_attributes = True