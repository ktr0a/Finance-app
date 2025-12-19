from __future__ import annotations

from fastapi import APIRouter, Depends

from api_server.deps import get_finance_service
from api_server.schemas import SummaryOut
from api_server.services.finance_service import FinanceService

router = APIRouter(prefix="/saves/{save_id}/summary", tags=["summary"])


@router.get("", response_model=SummaryOut)
def get_summary(
    save_id: str,
    service: FinanceService = Depends(get_finance_service),
) -> SummaryOut:
    data = service.summary(save_id)
    return SummaryOut(**data)
