
from pydantic import BaseModel

class TrainResponse(BaseModel):
    id: int
    train_number: str
    name: str
    total_seats: int
    
    class Config:
        from_attributes = True