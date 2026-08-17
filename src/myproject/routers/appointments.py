
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from myproject.database import get_session
from myproject.schemas.appointments import AppointmentCreate, AppointmentRead
from myproject.services.appointment_service import (
    create_appointment,
    get_appointment,
    list_appointments,
)

router = APIRouter()


db_dep = Depends(get_session)

@router.get("/", response_model=list[AppointmentRead])
def read_appointments(db: Session = db_dep):
    objs = list_appointments(db)
    return [
        {
            "id": o.id,
            "patient_id": o.patient_id,
            "doctor_id": o.doctor_id,
            "appointment_start": o.start_time,
            "appointment_end": o.end_time,
        }
        for o in objs
    ]


@router.get("/{appointment_id}", response_model=AppointmentRead)
def read_appointment(appointment_id: int, db: Session = db_dep):
    obj = get_appointment(db, appointment_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return {
        "id": obj.id,
        "patient_id": obj.patient_id,
        "doctor_id": obj.doctor_id,
        "appointment_start": obj.start_time,
        "appointment_end": obj.end_time,
    }


@router.post("/", response_model=AppointmentRead)
def create_appointment_endpoint(payload: AppointmentCreate, db: Session = db_dep):
    try:
        obj = create_appointment(db, payload)
        return {
            "id": obj.id,
            "patient_id": obj.patient_id,
            "doctor_id": obj.doctor_id,
            "appointment_start": obj.start_time,
            "appointment_end": obj.end_time,
        }
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
