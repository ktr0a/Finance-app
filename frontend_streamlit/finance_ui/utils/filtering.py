from __future__ import annotations

from typing import Any


def clean_summary_filters(f: dict[str, Any] | None) -> dict[str, Any]:
    """
    Keep only keys supported by Summary endpoint and drop None/empty.
    """
    if not isinstance(f, dict):
        return {}
    keep = ["q", "type", "category", "date_from", "date_to"]
    out: dict[str, Any] = {}
    for k in keep:
        v = f.get(k)
        if v is None:
            continue
        if isinstance(v, str) and not v.strip():
            continue
        out[k] = v
    return out
