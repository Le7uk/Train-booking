from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import auth , trains , bookings


app = FastAPI(title="Train Booking API")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(trains.router)
app.include_router(bookings.router)

@app.get("/")
def root():
    return {"message": "Train Booking API"}