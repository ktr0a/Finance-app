from __future__ import annotations

import uuid
from typing import Iterable, Tuple


def ensure_ids(transactions: list[dict]) -> Tuple[list[dict], bool]:
    """Ensure every transaction has a unique string id."""
    changed = False
    seen: set[str] = set()

    for tx in transactions:
        tx_id = tx.get("id")
        if not isinstance(tx_id, str) or not tx_id:
            tx_id = str(uuid.uuid4())
            tx["id"] = tx_id
            changed = True

        if tx_id in seen:
            tx_id = str(uuid.uuid4())
            tx["id"] = tx_id
            changed = True

        seen.add(tx_id)

    return transactions, changed
