from fastapi import FastAPI

from myproject.database import init_db
from myproject.routers.appointments import router as appointments_router
from myproject.routers.doctors import router as doctors_router
from myproject.routers.patients import router as patients_router

app = FastAPI(title="My Project API")


@app.on_event("startup")
def on_startup():
    # Ensure tables exist
    init_db()


app.include_router(patients_router, prefix="/patients", tags=["patients"])
app.include_router(doctors_router, prefix="/doctors", tags=["doctors"])
app.include_router(appointments_router, prefix="/appointments", tags=["appointments"])
