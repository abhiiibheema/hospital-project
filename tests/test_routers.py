from datetime import UTC, datetime, timedelta

from fastapi.testclient import TestClient

from myproject.database import get_session
from myproject.main import app


def test_routers_crud_and_errors():
    # Create a temporary file-backed SQLite DB so TestClient and sessions share schema
    import tempfile

    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker

    from myproject.models.models import Base

    with tempfile.NamedTemporaryFile(delete=False) as tf:
        db_url = f"sqlite:///{tf.name}"
        engine = create_engine(db_url, connect_args={"check_same_thread": False}, future=True)
        Base.metadata.create_all(bind=engine)
        SessionLocal = sessionmaker(bind=engine, future=True)

        def _override_session():
            db = SessionLocal()
            try:
                yield db
            finally:
                db.close()

        app.dependency_overrides[get_session] = _override_session
        client = TestClient(app)

        # Create patient
        patient_payload = {"name": "Alice", "email": "alice@example.com", "phone": "12345"}
        r = client.post("/patients/", json=patient_payload)
        assert r.status_code == 200
        patient = r.json()
        assert "id" in patient

        # Create doctor
        doctor_payload = {"name": "Dr Bob", "specialization": "General"}
        r = client.post("/doctors/", json=doctor_payload)
        assert r.status_code == 200
        doctor = r.json()
        assert "id" in doctor

        # Create appointment
        start = datetime.now(UTC)
        end = start + timedelta(hours=1)
        ap_payload = {
            "patient_id": patient["id"],
            "doctor_id": doctor["id"],
            "appointment_start": start.isoformat(),
            "appointment_end": end.isoformat(),
        }
        r = client.post("/appointments/", json=ap_payload)
        assert r.status_code == 200
        ap = r.json()
        assert ap["patient_id"] == patient["id"]

        # Get appointment
        r = client.get(f"/appointments/{ap['id']}")
        assert r.status_code == 200

        # Try to get non-existent patient/doctor/appointment -> 404
        r = client.get("/patients/9999")
        assert r.status_code == 404
        r = client.get("/doctors/9999")
        assert r.status_code == 404
        r = client.get("/appointments/9999")
        assert r.status_code == 404

        # Overlapping appointment should be rejected
        overlap_payload = {
            "patient_id": patient["id"],
            "doctor_id": doctor["id"],
            "appointment_start": (start + timedelta(minutes=30)).isoformat(),
            "appointment_end": (end + timedelta(hours=1)).isoformat(),
        }
        r = client.post("/appointments/", json=overlap_payload)
        assert r.status_code == 400
