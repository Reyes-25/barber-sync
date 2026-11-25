from barbersync.database import SessionLocal, engine
from barbersync.models import Barber, Base, Service


def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        if db.query(Service).first():
            return

        barbers = [
            Barber(name="Carlos", active=True),
            Barber(name="Luis", active=True),
        ]
        db.add_all(barbers)

        services = [
            Service(name="Corte", duration_minutes=30, price_cents=800),
            Service(name="Barba", duration_minutes=20, price_cents=500),
            Service(name="Corte + Barba", duration_minutes=45, price_cents=1200),
        ]
        db.add_all(services)

        db.commit()
    finally:
        db.close()


if __name__ == "__main__":
    seed()
