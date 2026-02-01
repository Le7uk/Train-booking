from .database import engine, SessionLocal
from .models import Base, Train, Route, User
from .utils.security import hash_password
from datetime import datetime, timedelta

Base.metadata.create_all(bind=engine)

def seed_data():
    db = SessionLocal()
    try:
        admin = db.query(User).filter(User.email == "admin@gmail.com").first()
        if not admin:
            admin = User(
                email="admin@gmail.com",
                password_hash=hash_password("wsizedupl"),
                role="admin"
            )
            db.add(admin)
            db.commit()
            print("Admin user created: admin@gmail.com")

        trains_data = [
            {"train_number": "001", "name": "Intercity Kyiv-Lviv", "total_seats": 200},
            {"train_number": "002", "name": "Express Kyiv-Odesa", "total_seats": 150},
            {"train_number": "003", "name": "Intercity Kyiv-Kharkiv", "total_seats": 180},
        ]
        for train_data in trains_data:
            existing = db.query(Train).filter(Train.train_number == train_data["train_number"]).first()
            if not existing:
                train = Train(**train_data)
                db.add(train)
        db.commit()

        routes_data = [
            {
                "train_id": 1,
                "from_station": "Kyiv",
                "to_station": "Lviv",
                "departure_time": datetime.now() + timedelta(days=1, hours=8),
                "arrival_time": datetime.now() + timedelta(days=1, hours=14),
                "price": 450.0,
                "available_seats": 200
            },
        ]
        for route_data in routes_data:
            existing = db.query(Route).filter(
                Route.train_id == route_data["train_id"],
                Route.from_station == route_data["from_station"],
                Route.to_station == route_data["to_station"],
                Route.departure_time == route_data["departure_time"]
            ).first()
            if not existing:
                route = Route(**route_data)
                db.add(route)
        db.commit()
        print("Seed data completed")
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()
