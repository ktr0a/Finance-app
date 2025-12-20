from __future__ import annotations

import re


_SAVE_ID_RE = re.compile(r"^[A-Za-z0-9_-]+$")


def is_valid_save_id(value: str) -> bool:
    v = value.strip()
    if not v:
        return False
    return _SAVE_ID_RE.match(v) is not None
