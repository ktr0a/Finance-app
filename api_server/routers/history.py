from __future__ import annotations

from fastapi import APIRouter, Depends

from api_server.deps import get_finance_service
from api_server.schemas import HistoryOut
from api_server.services.finance_service import FinanceService

router = APIRouter(prefix="/saves/{save_id}", tags=["history"])


@router.post("/undo")
def undo(
    save_id: str,
    service: FinanceService = Depends(get_finance_service),
) -> dict:
    service.undo(save_id)
    return {"ok": True, "message": "undone"}


@router.post("/redo")
def redo(
    save_id: str,
    service: FinanceService = Depends(get_finance_service),
) -> dict:
    service.redo(save_id)
    return {"ok": True, "message": "redone"}


@router.get("/history", response_model=HistoryOut)
def history(
    save_id: str,
    service: FinanceService = Depends(get_finance_service),
) -> HistoryOut:
    data = service.history(save_id)
    return HistoryOut(**data)
