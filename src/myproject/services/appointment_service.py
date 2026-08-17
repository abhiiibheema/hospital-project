from sqlalchemy.orm import Session

from myproject.models.models import Appointment
from myproject.schemas.appointments import AppointmentCreate


def list_appointments(db: Session):
    return db.query(Appointment).all()


def get_appointment(db: Session, appointment_id: int):
    return db.query(Appointment).filter(Appointment.id == appointment_id).first()


def create_appointment(db: Session, payload: AppointmentCreate):

    if payload.appointment_start >= payload.appointment_end:
        raise ValueError("appointment_start must be before appointment_end")


    overlap = (
        db.query(Appointment)
        .filter(
            Appointment.doctor_id == payload.doctor_id,
            Appointment.start_time < payload.appointment_end,
            Appointment.end_time > payload.appointment_start,
        )
        .first()
    )
    if overlap:
        raise ValueError("Overlapping appointment exists for this doctor")

    obj = Appointment(
        patient_id=payload.patient_id,
        doctor_id=payload.doctor_id,
        start_time=payload.appointment_start,
        end_time=payload.appointment_end,
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj
