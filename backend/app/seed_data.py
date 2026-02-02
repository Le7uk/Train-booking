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
            {"train_number": "PL001", "name": "Intercity Warsaw-Krakow", "total_seats": 200},
            {"train_number": "PL002", "name": "Express Warsaw-Gdansk", "total_seats": 150},
            {"train_number": "PL003", "name": "Intercity Krakow-Poznan", "total_seats": 180},
            {"train_number": "PL004", "name": "Express Gdansk-Wroclaw", "total_seats": 160},
            {"train_number": "PL005", "name": "Intercity Poznan-Szczecin", "total_seats": 140},
            {"train_number": "PL006", "name": "Express Wroclaw-Warsaw", "total_seats": 170},
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
                "from_station": "Warsaw",
                "to_station": "Krakow",
                "departure_time": datetime.now() + timedelta(days=1, hours=8),
                "arrival_time": datetime.now() + timedelta(days=1, hours=12),
                "price": 450.0,
                "available_seats": 200
            },
            {
                "train_id": 1,
                "from_station": "Warsaw",
                "to_station": "Krakow",
                "departure_time": datetime.now() + timedelta(days=2, hours=10),
                "arrival_time": datetime.now() + timedelta(days=2, hours=14),
                "price": 450.0,
                "available_seats": 200
            },
            {
                "train_id": 2,
                "from_station": "Warsaw",
                "to_station": "Gdansk",
                "departure_time": datetime.now() + timedelta(days=1, hours=9),
                "arrival_time": datetime.now() + timedelta(days=1, hours=15),
                "price": 380.0,
                "available_seats": 150
            },
            {
                "train_id": 2,
                "from_station": "Warsaw",
                "to_station": "Gdansk",
                "departure_time": datetime.now() + timedelta(days=3, hours=11),
                "arrival_time": datetime.now() + timedelta(days=3, hours=17),
                "price": 380.0,
                "available_seats": 150
            },
            {
                "train_id": 3,
                "from_station": "Krakow",
                "to_station": "Poznan",
                "departure_time": datetime.now() + timedelta(days=1, hours=7),
                "arrival_time": datetime.now() + timedelta(days=1, hours=13),
                "price": 420.0,
                "available_seats": 180
            },
            {
                "train_id": 3,
                "from_station": "Krakow",
                "to_station": "Poznan",
                "departure_time": datetime.now() + timedelta(days=4, hours=8),
                "arrival_time": datetime.now() + timedelta(days=4, hours=14),
                "price": 420.0,
                "available_seats": 180
            },
            {
                "train_id": 4,
                "from_station": "Gdansk",
                "to_station": "Wroclaw",
                "departure_time": datetime.now() + timedelta(days=2, hours=6),
                "arrival_time": datetime.now() + timedelta(days=2, hours=12),
                "price": 350.0,
                "available_seats": 160
            },
            {
                "train_id": 4,
                "from_station": "Gdansk",
                "to_station": "Wroclaw",
                "departure_time": datetime.now() + timedelta(days=5, hours=7),
                "arrival_time": datetime.now() + timedelta(days=5, hours=13),
                "price": 350.0,
                "available_seats": 160
            },
            {
                "train_id": 5,
                "from_station": "Poznan",
                "to_station": "Szczecin",
                "departure_time": datetime.now() + timedelta(days=1, hours=10),
                "arrival_time": datetime.now() + timedelta(days=1, hours=14),
                "price": 300.0,
                "available_seats": 140
            },
            {
                "train_id": 5,
                "from_station": "Poznan",
                "to_station": "Szczecin",
                "departure_time": datetime.now() + timedelta(days=3, hours=12),
                "arrival_time": datetime.now() + timedelta(days=3, hours=16),
                "price": 300.0,
                "available_seats": 140
            },
            {
                "train_id": 6,
                "from_station": "Wroclaw",
                "to_station": "Warsaw",
                "departure_time": datetime.now() + timedelta(days=2, hours=9),
                "arrival_time": datetime.now() + timedelta(days=2, hours=15),
                "price": 400.0,
                "available_seats": 170
            },
            {
                "train_id": 6,
                "from_station": "Wroclaw",
                "to_station": "Warsaw",
                "departure_time": datetime.now() + timedelta(days=4, hours=11),
                "arrival_time": datetime.now() + timedelta(days=4, hours=17),
                "price": 400.0,
                "available_seats": 170
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
