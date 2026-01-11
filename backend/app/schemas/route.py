
from pydantic import BaseModel
from datetime import datetime
from .train import TrainResponse

class RouteResponse(BaseModel):
    id: int
    train_id: int
    from_station: str
    to_station: str
    departure_time: datetime
    arrival_time: datetime
    price: float
    available_seats: int
    train: TrainResponse
    
    class Config:
        from_attributes = True