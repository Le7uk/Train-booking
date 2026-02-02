from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Route, Train, User
from ..schemas import RouteResponse, TrainResponse,RouteInput ,TrainInput
from ..utils.dependencies import get_admin_user


router = APIRouter(prefix="/api/admin", tags=["Admin"])

@router.post("/routes", response_model=RouteResponse)
def create_route(
    data: RouteInput,
    db: Session = Depends(get_db),
    admin: User = Depends(get_admin_user)
):
    print(f"Creating route with data: {data}")
    train = db.query(Train).filter(Train.id == data.train_id).first()
    if not train:
        print(f"Train with id {data.train_id} not found")
        raise HTTPException(status_code=404, detail="Train not found")

    new_route = Route(**data.model_dump())
    db.add(new_route)
    db.commit()
    db.refresh(new_route)
    print(f"Route created: {new_route}")
    return new_route

@router.delete("/routes/{route_id}")
def delete_route(
    route_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(get_admin_user)
):
    route = db.query(Route).filter(Route.id == route_id).first()
    if not route:
        raise HTTPException(status_code=404, detail="Route not found")
    
    db.delete(route)
    db.commit()
    return {"message": "Route deleted"}

@router.post("/trains", response_model=TrainResponse)
def create_train(
    data: TrainInput,
    db: Session = Depends(get_db),
    admin: User = Depends(get_admin_user)
):
    existing = db.query(Train).filter(Train.train_number == data.train_number).first()
    if existing:
        raise HTTPException(status_code=400, detail="Train number already exists")
    new_train = Train(**data.model_dump())
    db.add(new_train)
    db.commit()
    db.refresh(new_train)
    return new_train

@router.delete("/trains/{train_id}")
def delete_train(
    train_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(get_admin_user)
):
    train = db.query(Train).filter(Train.id == train_id).first()
    if not train:
        raise HTTPException(status_code=404, detail="Train not found")
    
    if train.routes:
        raise HTTPException(status_code=400, detail="Cannot delete train with existing routes")
    
    db.delete(train)
    db.commit()
    return {"message": "Train deleted"}

@router.get("/routes", response_model=list[RouteResponse])
def get_all_routes(
    db: Session = Depends(get_db),
    admin: User = Depends(get_admin_user)
):
    return db.query(Route).all()

@router.get("/trains", response_model=list[TrainResponse])
def get_all_trains(
    db: Session = Depends(get_db),
    admin: User = Depends(get_admin_user)
):
    return db.query(Train).all()

@router.post("/test")
def test_post():
    return {"message": "POST works!"}

