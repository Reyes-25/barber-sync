import os
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker

TEST_DATABASE_URL = "sqlite:///./test_barbersync.db"
os.environ["DATABASE_URL"] = TEST_DATABASE_URL

# Start each test run with a clean database file.
_db_path = Path("./test_barbersync.db").resolve()
if _db_path.exists():
    _db_path.unlink()

from barbersync.database import Base, get_db  # noqa: E402
from barbersync.main import app  # noqa: E402
from barbersync.models import Barber, Service  # noqa: E402

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
)


@event.listens_for(engine, "connect")
def _set_pragma(dbapi_conn, _record):
    cursor = dbapi_conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON")
    cursor.close()


TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="function")
def db_session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def seeded_db(db_session):
    barbers = [Barber(name="Carlos", active=True), Barber(name="Luis", active=True)]
    services = [
        Service(name="Corte", duration_minutes=30, price_cents=800),
        Service(name="Barba", duration_minutes=20, price_cents=500),
    ]
    db_session.add_all(barbers + services)
    db_session.commit()
    for obj in barbers + services:
        db_session.refresh(obj)
    yield db_session


@pytest.fixture(scope="function")
def client(seeded_db):
    with TestClient(app) as c:
        yield c
