import re
from datetime import date, datetime, time, timedelta
from zoneinfo import ZoneInfo

from sqlalchemy.orm import Session

from barbersync.config import (
    CLOSE_TIME,
    OPEN_TIME,
    SLOT_MINUTES,
    TIMEZONE,
    WORK_DAYS,
)
from barbersync.database import SessionLocal
from barbersync.models import Appointment, Barber, Customer, Service

PANAMA = ZoneInfo(TIMEZONE)
UTC = ZoneInfo("UTC")


def now_in_timezone() -> datetime:
    return datetime.now(PANAMA)


def utc_to_panama_str(value: str) -> str:
    dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=UTC)
    panama = dt.astimezone(PANAMA)
    return panama.isoformat()


def panama_to_utc(value: datetime) -> datetime:
    if value.tzinfo is None:
        raise ValueError("La fecha debe incluir zona horaria")
    return value.astimezone(UTC)


def utc_now() -> datetime:
    return datetime.now(UTC)


def normalize_phone(phone: str) -> str:
    digits = re.sub(r"\D", "", phone.strip())
    if len(digits) == 8:
        return f"+507{digits}"
    if len(digits) == 11 and digits.startswith("507"):
        return f"+507{digits[3:]}"
    raise ValueError("Teléfono inválido: debe tener 8 dígitos locales o iniciar con +507")


def parse_local_time(value: str) -> time:
    return datetime.strptime(value, "%H:%M").time()


def format_price(price_cents: int) -> str:
    return f"{price_cents / 100:.2f}"


def _start_of_day_in_panama(d: date) -> datetime:
    return datetime(d.year, d.month, d.day, 0, 0, tzinfo=PANAMA)


def _end_of_day_in_panama(d: date) -> datetime:
    next_day = d + timedelta(days=1)
    return datetime(next_day.year, next_day.month, next_day.day, 0, 0, tzinfo=PANAMA)


def _assert_future(start_panama: datetime) -> None:
    if start_panama <= now_in_timezone():
        raise ValueError("La cita debe ser en el futuro")


def _assert_on_grid(start_panama: datetime) -> None:
    if start_panama.second != 0 or start_panama.microsecond != 0:
        raise ValueError("La hora debe tener segundos y microsegundos en cero")
    if start_panama.minute % SLOT_MINUTES != 0:
        raise ValueError(f"La hora debe coincidir con la cuadrícula de {SLOT_MINUTES} minutos")


def _assert_within_hours(start_panama: datetime, end_panama: datetime) -> None:
    if start_panama.weekday() not in WORK_DAYS:
        raise ValueError("No hay atención ese día de la semana")
    open_t = parse_local_time(OPEN_TIME)
    close_t = parse_local_time(CLOSE_TIME)
    open_dt = datetime.combine(start_panama.date(), open_t, tzinfo=PANAMA)
    close_dt = datetime.combine(start_panama.date(), close_t, tzinfo=PANAMA)
    if start_panama < open_dt or end_panama > close_dt:
        raise ValueError(f"La cita debe estar dentro del horario {OPEN_TIME}-{CLOSE_TIME}")


def _to_canonical_utc(dt: datetime) -> str:
    return dt.astimezone(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


# Read-only helpers ------------------------------------------------------------


def get_barber(db: Session, barber_id: int) -> Barber | None:
    return db.query(Barber).filter(Barber.id == barber_id).first()


def get_service(db: Session, service_id: int) -> Service | None:
    return db.query(Service).filter(Service.id == service_id).first()


def get_customer_by_phone(db: Session, phone: str) -> Customer | None:
    return db.query(Customer).filter(Customer.phone == phone).first()


def list_barbers(db: Session) -> list[Barber]:
    return db.query(Barber).filter(Barber.active.is_(True)).order_by(Barber.id).all()


def list_services(db: Session) -> list[Service]:
    return db.query(Service).order_by(Service.id).all()


def get_availability(db: Session, barber_id: int, service_id: int, for_date: date) -> dict:
    barber = get_barber(db, barber_id)
    if barber is None or not barber.active:
        raise ValueError("Barbero no encontrado o inactivo")
    service = get_service(db, service_id)
    if service is None:
        raise ValueError("Servicio no encontrado")

    if for_date < date.today():
        raise ValueError("La fecha no puede estar en el pasado")

    if for_date.weekday() not in WORK_DAYS:
        return {
            "barber_id": barber_id,
            "service_id": service_id,
            "date": for_date,
            "timezone": TIMEZONE,
            "slots": [],
        }

    open_t = parse_local_time(OPEN_TIME)
    close_t = parse_local_time(CLOSE_TIME)
    day_start = datetime.combine(for_date, open_t, tzinfo=PANAMA)
    day_end = datetime.combine(for_date, close_t, tzinfo=PANAMA)

    start_utc = _to_canonical_utc(day_start)
    end_utc = _to_canonical_utc(day_end)

    appointments = (
        db.query(Appointment)
        .filter(
            Appointment.barber_id == barber_id,
            Appointment.status == "confirmed",
            Appointment.start_time < end_utc,
            Appointment.end_time > start_utc,
        )
        .all()
    )

    occupied = [(a.start_time, a.end_time) for a in appointments]

    current = day_start
    duration = timedelta(minutes=service.duration_minutes)
    slots = []
    while current + duration <= day_end:
        slot_end = current + duration
        start_utc_str = _to_canonical_utc(current)
        end_utc_str = _to_canonical_utc(slot_end)
        if not any(
            start < end_utc_str and end > start_utc_str for start, end in occupied
        ):
            # Exclude slots that start in the past for today.
            if for_date == date.today() and current <= now_in_timezone():
                pass
            else:
                slots.append(current.strftime("%H:%M"))
        current += timedelta(minutes=SLOT_MINUTES)

    return {
        "barber_id": barber_id,
        "service_id": service_id,
        "date": for_date,
        "timezone": TIMEZONE,
        "slots": slots,
    }


# Write operations -------------------------------------------------------------


def _find_or_create_customer(db: Session, name: str, phone: str) -> Customer:
    normalized = normalize_phone(phone)
    customer = get_customer_by_phone(db, normalized)
    if customer:
        return customer
    customer = Customer(name=name.strip(), phone=normalized)
    db.add(customer)
    db.flush()
    db.refresh(customer)
    return customer


def create_appointment(data: dict) -> Appointment:
    barber_id = data["barber_id"]
    service_id = data["service_id"]
    start_panama = data["start_time"].astimezone(PANAMA)
    customer_in = data["customer"]

    _assert_on_grid(start_panama)
    _assert_future(start_panama)

    db = SessionLocal()
    try:
        barber = get_barber(db, barber_id)
        if barber is None:
            raise ValueError("Barbero no encontrado")
        if not barber.active:
            raise ValueError("Barbero inactivo")

        service = get_service(db, service_id)
        if service is None:
            raise ValueError("Servicio no encontrado")

        end_panama = start_panama + timedelta(minutes=service.duration_minutes)
        _assert_within_hours(start_panama, end_panama)

        start_utc = _to_canonical_utc(start_panama)
        end_utc = _to_canonical_utc(end_panama)

        overlapping = (
            db.query(Appointment)
            .filter(
                Appointment.barber_id == barber_id,
                Appointment.status == "confirmed",
                Appointment.start_time < end_utc,
                Appointment.end_time > start_utc,
            )
            .first()
        )
        if overlapping:
            raise ValueError("El horario ya está reservado para este barbero")

        customer = _find_or_create_customer(
            db, customer_in["name"], customer_in["phone"]
        )

        appointment = Appointment(
            barber_id=barber_id,
            customer_id=customer.id,
            service_id=service_id,
            start_time=start_utc,
            end_time=end_utc,
            status="confirmed",
            created_at=_to_canonical_utc(datetime.now(UTC)),
        )
        db.add(appointment)
        db.commit()
        db.refresh(appointment)
        return appointment
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def get_appointment(db: Session, appointment_id: int) -> Appointment | None:
    return db.query(Appointment).filter(Appointment.id == appointment_id).first()


def list_appointments(
    db: Session,
    *,
    for_date: date | None = None,
    barber_id: int | None = None,
    status: str | None = None,
    limit: int = 50,
    offset: int = 0,
) -> list[Appointment]:
    query = db.query(Appointment)
    if barber_id is not None:
        query = query.filter(Appointment.barber_id == barber_id)
    if status is not None:
        query = query.filter(Appointment.status == status)
    if for_date is not None:
        start = _to_canonical_utc(_start_of_day_in_panama(for_date))
        end = _to_canonical_utc(_end_of_day_in_panama(for_date))
        query = query.filter(Appointment.start_time >= start, Appointment.start_time < end)
    return (
        query.order_by(Appointment.start_time, Appointment.id)
        .offset(offset)
        .limit(limit)
        .all()
    )


def cancel_appointment(appointment_id: int) -> Appointment:
    db = SessionLocal()
    try:
        appointment = get_appointment(db, appointment_id)
        if appointment is None:
            raise ValueError("Cita no encontrada")
        if appointment.status == "cancelled":
            raise ValueError("La cita ya está cancelada")
        appointment.status = "cancelled"
        db.commit()
        db.refresh(appointment)
        return appointment
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
