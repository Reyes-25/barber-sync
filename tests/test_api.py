import concurrent.futures
import random
import time
from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo

from barbersync import services

PANAMA = ZoneInfo(services.TIMEZONE)


def _next_weekday(weekday: int) -> date:
    d = date.today() + timedelta(days=1)
    while d.weekday() != weekday:
        d += timedelta(days=1)
    return d


def test_list_barbers(client):
    res = client.get("/api/v1/barbers")
    assert res.status_code == 200
    data = res.json()
    assert len(data) == 2
    assert data[0]["name"] == "Carlos"


def test_list_services(client):
    res = client.get("/api/v1/services")
    assert res.status_code == 200
    data = res.json()
    assert len(data) == 2
    assert data[0]["price"] == "8.00"


def test_availability(client):
    monday = _next_weekday(0)
    res = client.get(
        f"/api/v1/barbers/1/availability?service_id=1&date={monday.isoformat()}"
    )
    assert res.status_code == 200
    data = res.json()
    assert data["slots"][0] == "09:00"
    assert "09:05" in data["slots"]


def test_availability_sunday_empty(client):
    sunday = _next_weekday(6)
    res = client.get(
        f"/api/v1/barbers/1/availability?service_id=1&date={sunday.isoformat()}"
    )
    assert res.status_code == 200
    assert res.json()["slots"] == []


def test_create_appointment(client):
    monday = _next_weekday(0)
    start = datetime(monday.year, monday.month, monday.day, 9, 0, tzinfo=PANAMA)
    res = client.post(
        "/api/v1/appointments",
        json={
            "barber_id": 1,
            "service_id": 1,
            "start_time": start.isoformat(),
            "customer": {"name": "Ana Pérez", "phone": "6000-0000"},
        },
    )
    assert res.status_code == 201
    data = res.json()
    assert data["status"] == "confirmed"
    assert data["start_time"].endswith("-05:00")


def test_double_booking_rejected(client):
    monday = _next_weekday(0)
    start = datetime(monday.year, monday.month, monday.day, 10, 0, tzinfo=PANAMA)
    first = client.post(
        "/api/v1/appointments",
        json={
            "barber_id": 1,
            "service_id": 1,
            "start_time": start.isoformat(),
            "customer": {"name": "A", "phone": "6111-1111"},
        },
    )
    assert first.status_code == 201

    second = client.post(
        "/api/v1/appointments",
        json={
            "barber_id": 1,
            "service_id": 1,
            "start_time": start.isoformat(),
            "customer": {"name": "B", "phone": "6222-2222"},
        },
    )
    assert second.status_code == 409


def test_partial_overlap_rejected(client):
    monday = _next_weekday(0)
    first_start = datetime(monday.year, monday.month, monday.day, 10, 0, tzinfo=PANAMA)
    second_start = datetime(monday.year, monday.month, monday.day, 10, 15, tzinfo=PANAMA)

    first = client.post(
        "/api/v1/appointments",
        json={
            "barber_id": 1,
            "service_id": 1,
            "start_time": first_start.isoformat(),
            "customer": {"name": "A", "phone": "6333-3333"},
        },
    )
    assert first.status_code == 201

    second = client.post(
        "/api/v1/appointments",
        json={
            "barber_id": 1,
            "service_id": 1,
            "start_time": second_start.isoformat(),
            "customer": {"name": "B", "phone": "6444-4444"},
        },
    )
    assert second.status_code == 409


def test_adjacent_appointments_allowed(client):
    monday = _next_weekday(0)
    first_start = datetime(monday.year, monday.month, monday.day, 10, 0, tzinfo=PANAMA)
    second_start = datetime(monday.year, monday.month, monday.day, 10, 30, tzinfo=PANAMA)

    first = client.post(
        "/api/v1/appointments",
        json={
            "barber_id": 1,
            "service_id": 1,
            "start_time": first_start.isoformat(),
            "customer": {"name": "A", "phone": "6555-5555"},
        },
    )
    assert first.status_code == 201

    second = client.post(
        "/api/v1/appointments",
        json={
            "barber_id": 1,
            "service_id": 1,
            "start_time": second_start.isoformat(),
            "customer": {"name": "B", "phone": "6666-6666"},
        },
    )
    assert second.status_code == 201


def test_different_barbers_allowed(client):
    monday = _next_weekday(0)
    start = datetime(monday.year, monday.month, monday.day, 10, 0, tzinfo=PANAMA)

    first = client.post(
        "/api/v1/appointments",
        json={
            "barber_id": 1,
            "service_id": 1,
            "start_time": start.isoformat(),
            "customer": {"name": "A", "phone": "6777-7777"},
        },
    )
    second = client.post(
        "/api/v1/appointments",
        json={
            "barber_id": 2,
            "service_id": 1,
            "start_time": start.isoformat(),
            "customer": {"name": "B", "phone": "6888-8888"},
        },
    )
    assert first.status_code == 201
    assert second.status_code == 201


def test_cancel_appointment(client):
    monday = _next_weekday(0)
    start = datetime(monday.year, monday.month, monday.day, 11, 0, tzinfo=PANAMA)
    create = client.post(
        "/api/v1/appointments",
        json={
            "barber_id": 1,
            "service_id": 1,
            "start_time": start.isoformat(),
            "customer": {"name": "C", "phone": "6999-9999"},
        },
    )
    assert create.status_code == 201
    appt_id = create.json()["id"]

    cancel = client.patch(f"/api/v1/appointments/{appt_id}/cancel")
    assert cancel.status_code == 200
    assert cancel.json()["status"] == "cancelled"

    get_appt = client.get(f"/api/v1/appointments/{appt_id}")
    assert get_appt.json()["status"] == "cancelled"


def test_invalid_phone(client):
    monday = _next_weekday(0)
    start = datetime(monday.year, monday.month, monday.day, 9, 0, tzinfo=PANAMA)
    res = client.post(
        "/api/v1/appointments",
        json={
            "barber_id": 1,
            "service_id": 1,
            "start_time": start.isoformat(),
            "customer": {"name": "X", "phone": "123"},
        },
    )
    assert res.status_code == 422


def test_naive_datetime_rejected(client):
    monday = _next_weekday(0)
    start = datetime(monday.year, monday.month, monday.day, 9, 0)
    res = client.post(
        "/api/v1/appointments",
        json={
            "barber_id": 1,
            "service_id": 1,
            "start_time": start.isoformat(),
            "customer": {"name": "X", "phone": "6000-0000"},
        },
    )
    assert res.status_code == 422


def test_get_appointment_not_found(client):
    res = client.get("/api/v1/appointments/9999")
    assert res.status_code == 404


def test_active_appointment_limit(client):
    monday = _next_weekday(0)
    start = datetime(monday.year, monday.month, monday.day, 9, 0, tzinfo=PANAMA)
    res = client.post(
        "/api/v1/appointments",
        json={
            "barber_id": 1,
            "service_id": 1,
            "start_time": start.isoformat(),
            "customer": {"name": "Límite", "phone": "7000-0000"},
        },
    )
    assert res.status_code == 201, res.text

    # Second active appointment for the same customer on the same day is rejected.
    second_start = datetime(monday.year, monday.month, monday.day, 10, 0, tzinfo=PANAMA)
    res = client.post(
        "/api/v1/appointments",
        json={
            "barber_id": 1,
            "service_id": 1,
            "start_time": second_start.isoformat(),
            "customer": {"name": "Límite", "phone": "7000-0000"},
        },
    )
    assert res.status_code == 409
    assert "reserva activa" in res.json()["detail"].lower()


def test_concurrent_double_booking(seeded_db):
    monday = _next_weekday(0)
    start = datetime(monday.year, monday.month, monday.day, 10, 0, tzinfo=PANAMA)
    payloads = [
        {
            "barber_id": 1,
            "service_id": 1,
            "start_time": start,
            "customer": {"name": "Concurrente A", "phone": "7111-1111"},
        },
        {
            "barber_id": 1,
            "service_id": 1,
            "start_time": start,
            "customer": {"name": "Concurrente B", "phone": "7222-2222"},
        },
    ]

    results = []
    exceptions = []

    def attempt(payload, idx):
        # Jitter to increase the chance of both threads entering together.
        time.sleep(random.uniform(0, 0.01))
        try:
            appointment = services.create_appointment(payload)
            results.append((idx, appointment))
        except Exception as exc:  # noqa: BLE001
            exceptions.append((idx, exc))

    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        futures = [executor.submit(attempt, p, i) for i, p in enumerate(payloads)]
        concurrent.futures.wait(futures)

    assert len(results) == 1, f"Expected one success, got {len(results)}"
    assert len(exceptions) == 1, f"Expected one failure, got {len(exceptions)}"

    db = services.SessionLocal()
    try:
        confirmed = (
            db.query(services.Appointment)
            .filter(
                services.Appointment.barber_id == 1,
                services.Appointment.status == "confirmed",
            )
            .all()
        )
        assert len(confirmed) == 1
    finally:
        db.close()
