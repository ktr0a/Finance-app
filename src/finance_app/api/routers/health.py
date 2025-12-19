from __future__ import annotations

from datetime import datetime
import os
import platform
import sys

from fastapi import APIRouter

from finance_app.infra.pdf.api import list_parsers

router = APIRouter(tags=["default"])


@router.get("/health")
def health() -> dict:
    notes: list[str] = []
    try:
        _ = list_parsers()
    except Exception:
        notes.append("PDF parser registry unavailable")

    return {
        "ok": True,
        "version": "0.1.0",
        "api_version": "1.0.0",
        "app_name": "Finance App API",
        "commit": os.getenv("FINANCE_APP_COMMIT"),
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "time": datetime.utcnow().isoformat() + "Z",
        "notes": notes,
    }
