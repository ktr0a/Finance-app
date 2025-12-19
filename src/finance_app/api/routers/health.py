from __future__ import annotations

from fastapi import APIRouter

router = APIRouter(tags=["default"])


@router.get("/health")
def health() -> dict:
    return {"ok": True}
