from __future__ import annotations

from finance_app.api.services.finance_service import FinanceService


def get_finance_service() -> FinanceService:
    return FinanceService()
