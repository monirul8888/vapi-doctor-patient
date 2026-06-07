from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

load_dotenv()
VAPI_PRIVATE_KEY = os.getenv("VAPI_PRIVATE_KEY")

from app.routes import appointments

app = FastAPI(title="Doctor Appointment System")

# Allow frontend Streamlit to call
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include appointment routes
app.include_router(appointments.router)