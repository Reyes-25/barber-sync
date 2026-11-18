from datetime import date, timedelta

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from barbersync import services
from barbersync.config import BASE_DIR, TIMEZONE
from barbersync.database import get_db

router = APIRouter()
templates = Jinja2Templates(directory=BASE_DIR / "templates")


def _default_date() -> date:
    tomorrow = date.today() + timedelta(days=1)
    while tomorrow.weekday() > 4:
        tomorrow += timedelta(days=1)
    return tomorrow


@router.get("/", response_class=HTMLResponse)
def index(request: Request, db: Session = Depends(get_db)):
    barbers = services.list_barbers(db)
    services_list = services.list_services(db)
    default_date = _default_date()
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "barbers": barbers,
            "services": services_list,
            "default_date": default_date.isoformat(),
            "timezone": TIMEZONE,
        },
    )


@router.get("/admin", response_class=HTMLResponse)
def admin(request: Request, db: Session = Depends(get_db)):
    appointments = services.list_appointments(db, limit=100)
    enriched = []
    for a in appointments:
        enriched.append(
            {
                "id": a.id,
                "barber_name": a.barber.name,
                "customer_name": a.customer.name,
                "customer_phone": a.customer.phone,
                "service_name": a.service.name,
                "start_time": services.utc_to_panama_str(a.start_time),
                "end_time": services.utc_to_panama_str(a.end_time),
                "status": a.status,
            }
        )
    return templates.TemplateResponse(
        "admin.html", {"request": request, "appointments": enriched}
    )
