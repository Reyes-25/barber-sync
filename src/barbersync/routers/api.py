from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from barbersync import services
from barbersync.config import MAX_PAGE_LIMIT
from barbersync.database import get_db
from barbersync.exceptions import ConflictError
from barbersync.models import Appointment
from barbersync.schemas import (
    AppointmentCreate,
    AppointmentOut,
    AppointmentStatusOut,
    AvailabilityOut,
    BarberOut,
    ServiceOut,
)

router = APIRouter(prefix="/api/v1")


def _to_appointment_out(appointment: Appointment) -> AppointmentOut:
    return AppointmentOut(
        id=appointment.id,
        barber_id=appointment.barber_id,
        service_id=appointment.service_id,
        customer_id=appointment.customer_id,
        start_time=services.utc_to_panama_str(appointment.start_time),
        end_time=services.utc_to_panama_str(appointment.end_time),
        status=appointment.status,
        created_at=services.utc_to_panama_str(appointment.created_at),
    )


def _to_service_out(service) -> ServiceOut:
    return ServiceOut(
        id=service.id,
        name=service.name,
        duration_minutes=service.duration_minutes,
        price=services.format_price(service.price_cents),
    )


@router.get("/barbers", response_model=list[BarberOut])
def get_barbers(db: Session = Depends(get_db)):
    return services.list_barbers(db)


@router.get("/services", response_model=list[ServiceOut])
def get_services(db: Session = Depends(get_db)):
    return [_to_service_out(s) for s in services.list_services(db)]


@router.get("/barbers/{barber_id}/availability", response_model=AvailabilityOut)
def get_availability(
    barber_id: int,
    service_id: int = Query(..., ge=1),
    for_date: date = Query(..., alias="date"),
    db: Session = Depends(get_db),
):
    try:
        return services.get_availability(db, barber_id, service_id, for_date)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.post("/appointments", response_model=AppointmentOut, status_code=201)
def create_appointment(payload: AppointmentCreate):
    try:
        appointment = services.create_appointment(payload.model_dump())
        return _to_appointment_out(appointment)
    except ConflictError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.get("/appointments/{appointment_id}", response_model=AppointmentOut)
def get_appointment(appointment_id: int, db: Session = Depends(get_db)):
    appointment = services.get_appointment(db, appointment_id)
    if appointment is None:
        raise HTTPException(status_code=404, detail="Cita no encontrada")
    return _to_appointment_out(appointment)


@router.get("/appointments", response_model=list[AppointmentOut])
def list_appointments(
    for_date: date | None = Query(None, alias="date"),
    barber_id: int | None = Query(None, ge=1),
    status: str | None = Query(None, pattern="^(confirmed|cancelled)$"),
    limit: int = Query(MAX_PAGE_LIMIT, ge=1, le=MAX_PAGE_LIMIT),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    appointments = services.list_appointments(
        db,
        for_date=for_date,
        barber_id=barber_id,
        status=status,
        limit=limit,
        offset=offset,
    )
    return [_to_appointment_out(a) for a in appointments]


@router.patch("/appointments/{appointment_id}/cancel", response_model=AppointmentStatusOut)
def cancel_appointment(appointment_id: int):
    try:
        appointment = services.cancel_appointment(appointment_id)
        return AppointmentStatusOut(id=appointment.id, status=appointment.status)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
