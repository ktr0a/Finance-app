"""Minimal core types (Phase 1)."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Result:
    ok: bool
    data: object | None = None
    error: Exception | None = None


TransactionDict = dict[str, object]
Transactions = list[TransactionDict]
