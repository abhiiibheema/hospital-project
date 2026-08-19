
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_session
from app.schemas.doctors import DoctorCreate, DoctorRead
from app.services.doctor_service import create_doctor, get_doctor, list_doctors

router = APIRouter()

# module-level dependency to avoid calling Depends() in defaults (B008)
db_dep = Depends(get_session)

@router.get("/", response_model=list[DoctorRead])
def read_doctors(db: Session = db_dep):
    return list_doctors(db)


@router.get("/{doctor_id}", response_model=DoctorRead)
def read_doctor(doctor_id: int, db: Session = db_dep):
    obj = get_doctor(db, doctor_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return obj


@router.post("/", response_model=DoctorRead)
def create_doctor_endpoint(payload: DoctorCreate, db: Session = db_dep):
    return create_doctor(db, payload)
