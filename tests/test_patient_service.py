from app.schemas.schemas import PatientCreate
from app.services.patient_service import (
    create_patient,
    get_patient,
    list_patients,
)


def test_patient_crud(db):
    payload = PatientCreate(name="Alice", email="alice@example.com", phone="555-1000")
    patient = create_patient(db, payload)
    assert patient.id is not None
    assert patient.name == "Alice"

    all_patients = list_patients(db)
    assert any(p.id == patient.id for p in all_patients)

    fetched = get_patient(db, patient.id)
    assert fetched.id == patient.id
