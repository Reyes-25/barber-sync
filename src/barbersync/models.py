from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Column,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import relationship

from barbersync.database import Base


class Barber(Base):
    __tablename__ = "barbers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    active = Column(Boolean, nullable=False, default=True)


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    phone = Column(String(15), nullable=False, unique=True)


class Service(Base):
    __tablename__ = "services"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    duration_minutes = Column(Integer, nullable=False)
    price_cents = Column(Integer, nullable=False)

    __table_args__ = (
        CheckConstraint("duration_minutes > 0", name="chk_duration_positive"),
        CheckConstraint("price_cents >= 0", name="chk_price_non_negative"),
    )


class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    barber_id = Column(Integer, ForeignKey("barbers.id", ondelete="RESTRICT"), nullable=False)
    customer_id = Column(Integer, ForeignKey("customers.id", ondelete="RESTRICT"), nullable=False)
    service_id = Column(Integer, ForeignKey("services.id", ondelete="RESTRICT"), nullable=False)
    start_time = Column(Text, nullable=False)
    end_time = Column(Text, nullable=False)
    status = Column(String(20), nullable=False, default="confirmed")
    created_at = Column(Text, nullable=False)

    barber = relationship("Barber")
    customer = relationship("Customer")
    service = relationship("Service")

    __table_args__ = (
        CheckConstraint("status IN ('confirmed', 'cancelled')", name="chk_status"),
        Index(
            "uq_barber_start_confirmed",
            "barber_id",
            "start_time",
            unique=True,
            sqlite_where=(status == "confirmed"),
        ),
    )
