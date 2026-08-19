from fastapi import FastAPI

from app.database import init_db
from app.routers.appointments import router as appointments_router
from app.routers.doctors import router as doctors_router
from app.routers.patients import router as patients_router

app = FastAPI(title="My Project API")


@app.on_event("startup")
def on_startup():
	init_db()


app.include_router(patients_router, prefix="/patients", tags=["patients"])
app.include_router(doctors_router, prefix="/doctors", tags=["doctors"])
app.include_router(appointments_router, prefix="/appointments", tags=["appointments"])
