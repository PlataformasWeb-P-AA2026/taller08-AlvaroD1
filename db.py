from __future__ import annotations

import os
from pathlib import Path

from sqlalchemy import create_engine

PROJECT_ROOT = Path(__file__).resolve().parent
DATA_DIR = PROJECT_ROOT / "data"
DEFAULT_SQLITE_PATH = DATA_DIR / "paises.db"


def get_database_url() -> str:
    return os.getenv("DATABASE_URL", f"sqlite:///{DEFAULT_SQLITE_PATH.as_posix()}")


def get_engine(echo: bool = False):
    url = get_database_url()
    if url.startswith("sqlite:///"):
        DATA_DIR.mkdir(parents=True, exist_ok=True)
    return create_engine(url, echo=echo, future=True)
