from sqlalchemy.orm import Session

from myproject.models.models import Patient
from myproject.schemas.schemas import PatientCreate


def list_patients(db: Session):
    return db.query(Patient).all()


def get_patient(db: Session, patient_id: int):
    return db.query(Patient).filter(Patient.id == patient_id).first()


def create_patient(db: Session, payload: PatientCreate):
    obj = Patient(**payload.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj
