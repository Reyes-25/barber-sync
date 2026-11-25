from datetime import date as date_type

from pydantic import AwareDatetime, BaseModel, ConfigDict, Field, field_validator


class BarberOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    active: bool


class ServiceOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    duration_minutes: int
    price: str


class CustomerIn(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    phone: str = Field(..., min_length=1, max_length=30)

    @field_validator("name")
    @classmethod
    def strip_name(cls, v: str) -> str:
        return v.strip()


class CustomerOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    phone: str


class AvailabilityOut(BaseModel):
    barber_id: int
    service_id: int
    date: date_type
    timezone: str
    slots: list[str]


class AppointmentCreate(BaseModel):
    barber_id: int = Field(..., ge=1)
    service_id: int = Field(..., ge=1)
    start_time: AwareDatetime
    customer: CustomerIn


class AppointmentOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    barber_id: int
    service_id: int
    customer_id: int
    start_time: str
    end_time: str
    status: str
    created_at: str


class AppointmentStatusOut(BaseModel):
    id: int
    status: str
