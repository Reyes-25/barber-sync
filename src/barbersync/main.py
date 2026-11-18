from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from barbersync.database import Base, engine
from barbersync.routers import api, views
from barbersync.seed import seed


def create_app() -> FastAPI:
    app = FastAPI(title="BarberSync", version="1.0.0")

    Base.metadata.create_all(bind=engine)
    seed()

    app.mount("/static", StaticFiles(directory="src/barbersync/static"), name="static")
    app.include_router(api.router)
    app.include_router(views.router)

    return app


app = create_app()
