from datetime import datetime

from pydantic import BaseModel, ConfigDict


class AppointmentBase(BaseModel):
    patient_id: int
    doctor_id: int


class AppointmentCreate(AppointmentBase):
    appointment_start: datetime
    appointment_end: datetime


class AppointmentRead(AppointmentBase):
    id: int
    appointment_start: datetime
    appointment_end: datetime

    model_config = ConfigDict()
