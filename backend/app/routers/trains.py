from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Route, Train
from ..schemas import RouteResponse
from datetime import datetime

router = APIRouter(prefix="/api/trains", tags=["Trains"])

@router.get("/routes", response_model=list[RouteResponse])
def search_routes(
    from_station: str = Query(...),
    to_station: str = Query(...),
    date: str = Query(None),  
    db: Session = Depends(get_db)
):
    query = db.query(Route).join(Train)
    
    
    query = query.filter(
        Route.from_station.ilike(f"%{from_station}%"),
        Route.to_station.ilike(f"%{to_station}%")
    )
    
    
    if date:
        date_obj = datetime.strptime(date, "%Y-%m-%d")
        query = query.filter(
            Route.departure_time >= date_obj,
            Route.departure_time < date_obj.replace(hour=23, minute=59)
        )
    
    routes = query.all()
    return routes

@router.get("/routes/{route_id}", response_model=RouteResponse)
def get_route(route_id: int, db: Session = Depends(get_db)):
    route = db.query(Route).filter(Route.id == route_id).first()
    if not route:
        raise HTTPException(status_code=404, detail="Route not found")
    return route

