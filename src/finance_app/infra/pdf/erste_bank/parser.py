from __future__ import annotations

from pathlib import Path
from typing import Any

from finance_app.infra.pdf.general_extract_rawdata import raw_extraction
from finance_app.infra.pdf import parameter as p
from finance_app.infra.pdf.erste_bank.erste_format_rawdata import (
    delete_blacklist,
    extract_markers,
    extract_words_in_markers,
    find_dateformat_in_blacklst,
    sort_to_transactions,
)
from finance_app.infra.pdf.erste_bank.erste_manual_data_mapper import map_transaction


def parse(pdf_path: str) -> list[tuple[dict[str, Any], dict[str, Any]]]:
    path = str(Path(pdf_path))
    total_wordlst = raw_extraction(path)

    markers = extract_markers(total_wordlst, p.MARKER_STR)
    if markers is None:
        raise ValueError("Markers not found (unsupported format or unexpected PDF layout)")

    valid_lst = extract_words_in_markers(total_wordlst, markers)
    tx_wordlists = sort_to_transactions(valid_lst, markers)

    cleaned, blacklst = delete_blacklist(tx_wordlists)
    year = find_dateformat_in_blacklst(blacklst)

    mapped: list[tuple[dict[str, Any], dict[str, Any]]] = []
    for item in cleaned:
        tx_dict, status_dict = map_transaction(item, markers, yr=year)
        mapped.append((tx_dict, status_dict))

    return mapped

