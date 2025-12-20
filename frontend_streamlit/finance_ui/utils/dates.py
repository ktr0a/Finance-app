from __future__ import annotations

from datetime import date, datetime
from typing import Any


_FMT = "%d.%m.%Y"


def to_api_date(d: date) -> str:
    return d.strftime(_FMT)


def from_api_date(s: str) -> date:
    return datetime.strptime(s, _FMT).date()


def safe_parse_date(value: Any) -> date | None:
    if isinstance(value, date):
        return value
    if isinstance(value, str):
        value = value.strip()
        if not value:
            return None
        try:
            return from_api_date(value)
        except ValueError:
            return None
    return None
