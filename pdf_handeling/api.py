"""Stable API boundary for PDF parsing (registry + parse)."""

from __future__ import annotations

from pathlib import Path
from typing import Callable

ParserFunc = Callable[[str], list[tuple[dict, dict]]]

_PARSERS: dict[str, tuple[str, ParserFunc]] = {}


def register_parser(parser_id: str, display_name: str, func: ParserFunc) -> None:
    _PARSERS[parser_id] = (display_name, func)


def _ensure_registry() -> None:
    if _PARSERS:
        return

    from pdf_handeling.erste_bank.parser import parse as erste_parse

    register_parser("erste", "Erste Bank (MVP)", erste_parse)


def list_parsers() -> list[tuple[str, str]]:
    _ensure_registry()
    return [(key, display) for key, (display, _) in sorted(_PARSERS.items())]


def parse_pdf(pdf_path: str, parser_id: str = "auto") -> list[tuple[dict, dict]]:
    _ensure_registry()

    path = Path(pdf_path)
    if not path.exists():
        raise FileNotFoundError(str(path))

    if parser_id == "auto":
        parser_id = "erste" if "erste" in _PARSERS else sorted(_PARSERS.keys())[0]

    if parser_id not in _PARSERS:
        raise ValueError(f"Unknown parser_id: {parser_id}")

    _, parser_func = _PARSERS[parser_id]
    return parser_func(str(path))
