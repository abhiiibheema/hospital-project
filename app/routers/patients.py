
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_session
from app.schemas.schemas import PatientCreate, PatientRead
from app.services.patient_service import (
    create_patient,
    get_patient,
    list_patients,
)

router = APIRouter()

# module-level dependency to avoid calling Depends() in defaults (B008)
db_dep = Depends(get_session)

@router.get("/", response_model=list[PatientRead])
def read_patients(db: Session = db_dep):
    return list_patients(db)


@router.get("/{patient_id}", response_model=PatientRead)
def read_patient(patient_id: int, db: Session = db_dep):
    obj = get_patient(db, patient_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Patient not found")
    return obj


@router.post("/", response_model=PatientRead)
def create_patient_endpoint(payload: PatientCreate, db: Session = db_dep):
    return create_patient(db, payload)
