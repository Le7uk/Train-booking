from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import auth

app = FastAPI(title="Train Booking API")

# CORS (щоб фронтенд міг звертатись до API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Підключи роутери
app.include_router(auth.router)

@app.get("/")
def root():
    return {"message": "Train Booking API"}