
# 🚆 Train Booking System

A Python-based web application for managing train tickets, built with FastAPI and SQLite.

---

## 🧩 Development Phases

**Phase 1 & 2:**
Requirements defined and environment setup (Python 3.13 + FastAPI).

**Phase 3:**
Database schema implemented in SQLite with relational tables (Users, Trains, Routes, Bookings).

**Phase 4:**
User Authentication system with Role-Based Access Control (Admin/User) using 🔐 JWT.

**Phase 5:**
Complete User Booking Flow (Route search → Seat selection → Booking confirmation).

**Phase 6:**
Admin Management Panel with database maintenance features (Add/Delete routes and trains).

---

## 🛠️ Tech Stack

**Frontend:** HTML, CSS, JavaScript

**Backend:** FastAPI (Python 3.13)

**Database:** SQLite

**Libraries:**
SQLAlchemy, Pydantic, Pydantic-Settings, Python-JOSE, PassLib, Uvicorn

---

## 📖 How to Run

Clone the repository and navigate to the project folder.

(Recommended) Create and activate a virtual environment.

Run:

```bash
pip install -r requirements.txt
```

Seed the database:

```bash
python -m app.seed_data
```

(Admin user: `admin@gmail.com` / `wsizedupl`)

Start the backend server:

```bash
uvicorn app.main:app --reload
```

```bash
python -m http.server 8080 (for example)
```

---

## 📁 Project Structure

**backend:** FastAPI backend with routers, models, schemas, and utilities.
**frontend:** HTML/CSS/JS frontend with pages for login, registration, booking, and admin panel.

---

## 🔐 Features

* User registration and login with JWT authentication
* Route search with filters (from/to/date)
* Seat booking with real-time availability
* Admin panel for managing routes and trains
* Responsive UI with clean design

---

Enjoy your train booking experience! 🎫

---
