from pydantic import BaseModel

class TrainInput(BaseModel):
    train_number: str 
    name: str
    total_seats: int
