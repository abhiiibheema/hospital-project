from app.schemas.doctors import DoctorCreate
from app.services.doctor_service import create_doctor, get_doctor, list_doctors


def test_doctor_crud(db):
    payload = DoctorCreate(name="Dr. Bob", specialization="Cardiology")
    doctor = create_doctor(db, payload)
    assert doctor.id is not None
    assert doctor.name == "Dr. Bob"

    all_doctors = list_doctors(db)
    assert any(d.id == doctor.id for d in all_doctors)

    fetched = get_doctor(db, doctor.id)
    assert fetched.id == doctor.id
