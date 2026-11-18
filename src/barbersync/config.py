import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./barbersync.db")
TIMEZONE = "America/Panama"

OPEN_TIME = "09:00"
CLOSE_TIME = "18:00"
WORK_DAYS = {0, 1, 2, 3, 4, 5}  # Monday-Saturday
SLOT_MINUTES = 5
WRITE_TIMEOUT_SECONDS = int(os.getenv("WRITE_TIMEOUT_SECONDS", "5"))

DEFAULT_PAGE_LIMIT = 50
MAX_PAGE_LIMIT = 100
