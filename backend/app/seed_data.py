from database import engine, SessionLocal
from models import Base, Train, Route, User
from datetime import datetime, timedelta
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Створи таблиці
Base.metadata.create_all(bind=engine)

db = SessionLocal()

# Додай тестового юзера
test_user = User(
    email="test@test.com",
    password_hash=pwd_context.hash("password123")
)
db.add(test_user)

# Додай поїзди
trains_data = [
    {"train_number": "001", "name": "Intercity Kyiv-Lviv", "total_seats": 200},
    {"train_number": "002", "name": "Express Kyiv-Odesa", "total_seats": 150},
    {"train_number": "003", "name": "Intercity Kyiv-Kharkiv", "total_seats": 180},
]

for train_data in trains_data:
    train = Train(**train_data)
    db.add(train)

db.commit()

# Додай маршрути
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
    {
        "train_id": 1,
        "from_station": "Kyiv",
        "to_station": "Lviv",
        "departure_time": datetime.now() + timedelta(days=2, hours=10),
        "arrival_time": datetime.now() + timedelta(days=2, hours=16),
        "price": 450.0,
        "available_seats": 200
    },
    {
        "train_id": 2,
        "from_station": "Kyiv",
        "to_station": "Odesa",
        "departure_time": datetime.now() + timedelta(days=1, hours=9),
        "arrival_time": datetime.now() + timedelta(days=1, hours=15),
        "price": 380.0,
        "available_seats": 150
    },
]

for route_data in routes_data:
    route = Route(**route_data)
    db.add(route)

db.commit()
db.close()

print("✅ База даних створена і заповнена тестовими даними!")