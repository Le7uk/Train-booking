from pydantic import BaseModel, ConfigDict
from datetime import datetime
from .route import RouteResponse

class BookingCreate(BaseModel):
    route_id: int
    carriage: int  
    seat_number: int

class BookingResponse(BaseModel):
    id: int
    user_id: int
    route_id: int
    carriage: int  
    seat_number: int
    booking_date: datetime
    status: str
    route: RouteResponse
    
    model_config = ConfigDict(from_attributes=True)