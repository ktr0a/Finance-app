from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class ApiError(Exception):
    message: str
    status_code: int | None = None
    detail: Any | None = None

    def __str__(self) -> str:
        base = self.message
        if self.status_code is not None:
            base = f"{base} (HTTP {self.status_code})"
        return base
