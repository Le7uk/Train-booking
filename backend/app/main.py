from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import auth , trains , bookings


app = FastAPI(title="Train Booking API")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)

app.include_router(auth.router)
app.include_router(trains.router)
app.include_router(bookings.router)

@app.get("/")
def root():
    return {"message": "Train Booking API"}