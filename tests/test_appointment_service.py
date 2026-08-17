from datetime import UTC, datetime, timedelta

from myproject.schemas.appointments import AppointmentCreate
from myproject.schemas.doctors import DoctorCreate
from myproject.schemas.schemas import PatientCreate
from myproject.services.appointment_service import (
    create_appointment,
    get_appointment,
    list_appointments,
)
from myproject.services.doctor_service import create_doctor
from myproject.services.patient_service import create_patient


def test_appointment_creation_and_overlap(db):
    # create supporting patient and doctor
    p = create_patient(db, PatientCreate(name="Carol", email="carol@example.com", phone="555-2000"))
    d = create_doctor(db, DoctorCreate(name="Dr. Eve", specialization="Dermatology"))

    start1 = datetime.now(UTC)
    end1 = start1 + timedelta(hours=1)

    ap1_payload = AppointmentCreate(patient_id=p.id, doctor_id=d.id, appointment_start=start1, appointment_end=end1)
    ap1 = create_appointment(db, ap1_payload)
    assert ap1.id is not None

    # overlapping appointment (starts before ap1 ends and ends after ap1 starts)
    overlap_start = start1 + timedelta(minutes=30)
    overlap_end = overlap_start + timedelta(hours=1)
    ap2_payload = AppointmentCreate(patient_id=p.id, doctor_id=d.id, appointment_start=overlap_start, appointment_end=overlap_end)
    import pytest
    with pytest.raises(ValueError):
        create_appointment(db, ap2_payload)

    # non-overlapping appointment (starts after ap1 ends)
    non_overlap_start = end1 + timedelta(minutes=1)
    non_overlap_end = non_overlap_start + timedelta(hours=1)
    ap3_payload = AppointmentCreate(patient_id=p.id, doctor_id=d.id, appointment_start=non_overlap_start, appointment_end=non_overlap_end)
    ap3 = create_appointment(db, ap3_payload)
    assert ap3.id is not None

    # list and get
    apps = list_appointments(db)
    assert any(a.id == ap1.id for a in apps)
    assert any(a.id == ap3.id for a in apps)

    fetched = get_appointment(db, ap1.id)
    assert fetched.id == ap1.id
