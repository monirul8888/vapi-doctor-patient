import datetime as dt
import os
import requests
from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Appointment
from app.schemas import (
    AppointmentRequest,
    AppointmentResponse,
    CancelAppointmentRequest,
    CancelAppointmentResponse,
    ListAppointmentRequest
)

# Load private key from .env
VAPI_PRIVATE_KEY = os.getenv("VAPI_PRIVATE_KEY")
VAPI_ASSISTANT_ID = os.getenv("VAPI_ASSISTANT_ID")

router = APIRouter(tags=["Appointments"])

# Helper: server-side call to Vapi
def notify_vapi_server(appointment: AppointmentResponse):
    url = f"https://api.vapi.ai/assistant/{VAPI_ASSISTANT_ID}/events"
    payload = {
        "event": "appointment_scheduled",
        "data": {
            "appointment_id": appointment.id,
            "patient_name": appointment.patient_name,
            "reason": appointment.reason,
            "start_time": appointment.start_time.isoformat()
        }
    }
    headers = {
        "Authorization": f"Bearer {VAPI_PRIVATE_KEY}",
        "Content-Type": "application/json"
    }
    try:
        requests.post(url, headers=headers, json=payload, timeout=10)
    except Exception as e:
        print(f"[VAPI] Error sending server-side event: {e}")


# POST endpoints
@router.post("/schedule_appointment/", response_model=AppointmentResponse)
def schedule_appointment(request: AppointmentRequest, db: Session = Depends(get_db)):
    existing = db.query(Appointment).filter(
        Appointment.start_time == request.start_time,
        Appointment.canceled == False
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="This appointment slot is already booked.")

    new_appointment = Appointment(
        patient_name=request.patient_name,
        reason=request.reason,
        start_time=request.start_time
    )
    db.add(new_appointment)
    db.commit()
    db.refresh(new_appointment)

    # Notify Vapi server-side
    notify_vapi_server(new_appointment)

    return new_appointment


@router.post("/cancel_appointment/", response_model=CancelAppointmentResponse)
def cancel_appointment(request: CancelAppointmentRequest, db: Session = Depends(get_db)):
    start_dt = dt.datetime.combine(request.date, dt.time.min)
    end_dt = start_dt + dt.timedelta(days=1)

    appointments = db.query(Appointment).filter(
        Appointment.patient_name == request.patient_name,
        Appointment.start_time >= start_dt,
        Appointment.start_time < end_dt,
        Appointment.canceled == False
    ).all()

    if not appointments:
        raise HTTPException(status_code=404, detail="No matching appointment found")

    for a in appointments:
        a.canceled = True
    db.commit()
    return CancelAppointmentResponse(canceled_count=len(appointments))


@router.post("/list_appointments/", response_model=list[AppointmentResponse])
def list_appointments(request: ListAppointmentRequest, db: Session = Depends(get_db)):
    start_dt = dt.datetime.combine(request.date, dt.time.min)
    end_dt = start_dt + dt.timedelta(days=1)

    appointments = db.query(Appointment).filter(
        Appointment.start_time >= start_dt,
        Appointment.start_time < end_dt,
        Appointment.canceled == False
    ).order_by(Appointment.start_time.asc()).all()

    return appointments


# GET endpoints
@router.get("/appointments/{appointment_id}", response_model=AppointmentResponse)
def get_appointment_by_id(appointment_id: int = Path(..., description="Appointment ID"), db: Session = Depends(get_db)):
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return appointment


@router.get("/appointments/patient/{patient_name}", response_model=list[AppointmentResponse])
def get_appointments_by_patient(patient_name: str, db: Session = Depends(get_db)):
    appointments = db.query(Appointment).filter(
        Appointment.patient_name == patient_name
    ).order_by(Appointment.start_time.asc()).all()
    if not appointments:
        raise HTTPException(status_code=404, detail="No appointments found for this patient")
    return appointments


@router.get("/appointments/date/{date}", response_model=list[AppointmentResponse])
def get_appointments_by_date(date: str, db: Session = Depends(get_db)):
    try:
        start_dt = dt.datetime.fromisoformat(date)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format, use YYYY-MM-DD")

    end_dt = start_dt + dt.timedelta(days=1)

    appointments = db.query(Appointment).filter(
        Appointment.start_time >= start_dt,
        Appointment.start_time < end_dt,
        Appointment.canceled == False
    ).order_by(Appointment.start_time.asc()).all()
    return appointments