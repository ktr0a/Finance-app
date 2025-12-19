from __future__ import annotations

from fastapi import APIRouter, Depends, Query

from api_server.deps import get_finance_service
from api_server.schemas import (
    TransactionCreate,
    TransactionOut,
    TransactionUpdate,
    TransactionsPage,
)
from api_server.services.finance_service import FinanceService

router = APIRouter(prefix="/saves/{save_id}/transactions", tags=["transactions"])


def _model_to_dict(model) -> dict:
    if hasattr(model, "model_dump"):
        return model.model_dump()
    return model.dict()


@router.get("", response_model=TransactionsPage)
def list_transactions(
    save_id: str,
    q: str | None = None,
    type: str | None = None,
    category: str | None = None,
    date_from: str | None = None,
    date_to: str | None = None,
    sort: str | None = None,
    order: str | None = None,
    limit: int = Query(200),
    offset: int = Query(0),
    service: FinanceService = Depends(get_finance_service),
) -> TransactionsPage:
    result = service.list_transactions(
        save_id,
        q=q,
        type=type,
        category=category,
        date_from=date_from,
        date_to=date_to,
        sort=sort,
        order=order,
        limit=limit,
        offset=offset,
    )
    return TransactionsPage(
        items=result.items,
        total=result.total,
        limit=result.limit,
        offset=result.offset,
    )


@router.get("/{tx_id}", response_model=TransactionOut)
def get_transaction(
    save_id: str,
    tx_id: str,
    service: FinanceService = Depends(get_finance_service),
) -> TransactionOut:
    tx = service.get_transaction(save_id, tx_id)
    return TransactionOut(**tx)


@router.post("", response_model=TransactionOut)
def create_transaction(
    save_id: str,
    body: TransactionCreate,
    service: FinanceService = Depends(get_finance_service),
) -> TransactionOut:
    created = service.create_transaction(save_id, _model_to_dict(body))
    return TransactionOut(**created)


@router.put("/{tx_id}", response_model=TransactionOut)
def update_transaction(
    save_id: str,
    tx_id: str,
    body: TransactionUpdate,
    service: FinanceService = Depends(get_finance_service),
) -> TransactionOut:
    updated = service.update_transaction(save_id, tx_id, _model_to_dict(body))
    return TransactionOut(**updated)


@router.delete("/{tx_id}")
def delete_transaction(
    save_id: str,
    tx_id: str,
    service: FinanceService = Depends(get_finance_service),
) -> dict:
    service.delete_transaction(save_id, tx_id)
    return {"deleted": True}
