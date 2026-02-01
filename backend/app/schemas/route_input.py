from pydantic import BaseModel
from datetime import datetime

class RouteInput(BaseModel):
    train_id: int
    from_station: str
    to_station: str
    departure_time: datetime
    arrival_time: datetime
    price: float
    available_seats: int
