from __future__ import annotations

from api_server.services.finance_service import FinanceService


def get_finance_service() -> FinanceService:
    return FinanceService()
