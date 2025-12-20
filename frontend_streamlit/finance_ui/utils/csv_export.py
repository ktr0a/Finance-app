from __future__ import annotations

import csv
import io
from typing import Any


def transactions_to_csv_bytes(items: list[dict[str, Any]]) -> bytes:
    """
    Frontend-side CSV export. Uses a stable column order.
    """
    cols = ["date", "name", "category", "type", "amount", "id"]
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=cols, extrasaction="ignore")
    w.writeheader()
    for it in items:
        w.writerow({k: it.get(k, "") for k in cols})
    return buf.getvalue().encode("utf-8")
