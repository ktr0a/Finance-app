from __future__ import annotations

from typing import Literal, TypedDict


class SaveInfo(TypedDict, total=False):
    save_id: str
    filename: str
    updated_at: str | None
    tx_count: int | None


TxType = Literal["I", "E"]


class Transaction(TypedDict):
    name: str
    category: str
    type: TxType
    amount: float
    date: str  # DD.MM.YYYY


class TransactionOut(Transaction):
    id: str
