from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Booking, Route, User
from ..schemas import BookingCreate, BookingResponse
from ..utils.dependencies import get_current_user

router = APIRouter(prefix="/api/bookings", tags=["Bookings"])

@router.get("/my", response_model=list[BookingResponse])
def get_my_bookings(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Отримати мої бронювання"""
    bookings = db.query(Booking).filter(
        Booking.user_id == current_user.id
    ).all()
    return bookings

@router.get("/occupied/{route_id}")
def get_occupied_seats(route_id: int, db: Session = Depends(get_db)):

    bookings = db.query(Booking).filter(
        Booking.route_id == route_id,
        Booking.status == "active"
    ).all()
    
    occupied = [
        {"carriage": b.carriage, "seat": b.seat_number} 
        for b in bookings
    ]
    
    return {"occupied_seats": occupied}

@router.post("", response_model=BookingResponse)
def create_booking(
    booking_data: BookingCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    route = db.query(Route).filter(Route.id == booking_data.route_id).first()
    if not route:
        raise HTTPException(status_code=404, detail="Route not found")
    
    if route.available_seats <= 0:
        raise HTTPException(status_code=400, detail="No available seats")
    
    # Перевірка валідності вагону і місця
    if booking_data.carriage < 1 or booking_data.carriage > 10:
        raise HTTPException(status_code=400, detail="Carriage must be between 1-10")
    
    if booking_data.seat_number < 1 or booking_data.seat_number > 20:
        raise HTTPException(status_code=400, detail="Seat must be between 1-20")
    
    existing_booking = db.query(Booking).filter(
        Booking.route_id == booking_data.route_id,
        Booking.carriage == booking_data.carriage,
        Booking.seat_number == booking_data.seat_number,
        Booking.status == "active"
    ).first()
    
    if existing_booking:
        raise HTTPException(status_code=400, detail="This seat is already booked")
    
    new_booking = Booking(
        user_id=current_user.id,
        route_id=booking_data.route_id,
        carriage=booking_data.carriage,
        seat_number=booking_data.seat_number
    )
    
    route.available_seats -= 1
    
    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)
    
    return new_booking


@router.delete("/{booking_id}")
def cancel_booking(
    booking_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    booking = db.query(Booking).filter(
        Booking.id == booking_id,
        Booking.user_id == current_user.id
    ).first()
    
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    route = db.query(Route).filter(Route.id == booking.route_id).first()
    route.available_seats += 1
    
    booking.status = "cancelled"
    db.commit()
    
    return {"message": "Booking cancelled"}