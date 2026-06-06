import datetime as dt

from sqlalchemy import Boolean, Column, DateTime, Integer, String

from app.database import Base


class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    patient_name = Column(String, index=True, nullable=False)
    reason = Column(String, nullable=True)
    start_time = Column(DateTime, index=True, nullable=False)
    canceled = Column(Boolean, default=False)
    created_at = Column(DateTime, default=dt.datetime.utcnow)