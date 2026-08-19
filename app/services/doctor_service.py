from sqlalchemy.orm import Session

from app.models.models import Doctor
from app.schemas.doctors import DoctorCreate


def list_doctors(db: Session):
    return db.query(Doctor).all()


def get_doctor(db: Session, doctor_id: int):
    return db.query(Doctor).filter(Doctor.id == doctor_id).first()


def create_doctor(db: Session, payload: DoctorCreate):
    obj = Doctor(**payload.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj
