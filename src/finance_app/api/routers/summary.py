from __future__ import annotations

from fastapi import APIRouter, Depends, Query

from finance_app.api.deps import get_finance_service
from finance_app.api.schemas import SummaryOut
from finance_app.api.services.finance_service import FinanceService

router = APIRouter(prefix="/saves/{save_id}/summary", tags=["summary"])


@router.get("", response_model=SummaryOut)
def get_summary(
    save_id: str,
    q: str | None = Query(default=None),
    type: str | None = Query(default=None),
    category: str | None = Query(default=None),
    date_from: str | None = Query(default=None),
    date_to: str | None = Query(default=None),
    service: FinanceService = Depends(get_finance_service),
) -> SummaryOut:
    data = service.summary(
        save_id,
        q=q,
        type=type,
        category=category,
        date_from=date_from,
        date_to=date_to,
    )
    return SummaryOut(**data)
