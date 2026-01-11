from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Booking, Route, User
from ..schemas import BookingCreate, BookingResponse
from ..utils.dependencies import get_current_user

router = APIRouter(prefix="/api/bookings", tags=["Bookings"])

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
    
    existing_booking = db.query(Booking).filter(
        Booking.route_id == booking_data.route_id,
        Booking.seat_number == booking_data.seat_number,
        Booking.status == "active"
    ).first()
    
    if existing_booking:
        raise HTTPException(status_code=400, detail="Seat already booked")
    
    new_booking = Booking(
        user_id=current_user.id,
        route_id=booking_data.route_id,
        seat_number=booking_data.seat_number
    )
    
    route.available_seats -= 1
    
    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)
    
    return new_booking

@router.get("/my", response_model=list[BookingResponse])
def get_my_bookings(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    bookings = db.query(Booking).filter(
        Booking.user_id == current_user.id
    ).all()
    return bookings

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
    
    # Повернути місце
    route = db.query(Route).filter(Route.id == booking.route_id).first()
    route.available_seats += 1
    
    booking.status = "cancelled"
    db.commit()
    
    return {"message": "Booking cancelled"}