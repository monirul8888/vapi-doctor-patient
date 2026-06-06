from fastapi import FastAPI
from app.database import init_db
from app.routes.appointments import router as appointments_router

# Initialize DB on startup
init_db()

app = FastAPI(
    title="Hospital Appointment API",
    description="FastAPI + SQLAlchemy + PostgreSQL appointment system",
    version="1.0.0"
)

app.include_router(appointments_router)

@app.get("/")
def root():
    return {"message": "Hospital Appointment API is running"}