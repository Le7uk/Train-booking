from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    bookings = relationship("Booking", back_populates="user")
    
class Train(Base):
    __tablename__ = "trains"
    
    id = Column(Integer, primary_key=True, index=True)
    train_number = Column(String, unique=True)
    name = Column(String)
    total_seats = Column(Integer)
    
    routes = relationship("Route", back_populates="train")

class Route(Base):
    __tablename__ = "routes"
    
    id = Column(Integer, primary_key=True, index=True)
    train_id = Column(Integer, ForeignKey("trains.id"))
    from_station = Column(String)
    to_station = Column(String)
    departure_time = Column(DateTime)
    arrival_time = Column(DateTime)
    price = Column(Float)
    available_seats = Column(Integer)
    
    train = relationship("Train", back_populates="routes")
    bookings = relationship("Booking", back_populates="route")

class Booking(Base):
    __tablename__ = "bookings"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    route_id = Column(Integer, ForeignKey("routes.id"))
    seat_number = Column(Integer)
    booking_date = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default="active") 
    
    user = relationship("User", back_populates="bookings")
    route = relationship("Route", back_populates="bookings")