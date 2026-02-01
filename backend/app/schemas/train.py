from pydantic import BaseModel, ConfigDict

class TrainResponse(BaseModel):
    id: int
    train_number: str
    name: str
    total_seats: int
    
    model_config = ConfigDict(from_attributes=True)