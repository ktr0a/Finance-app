from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Sequence


@dataclass(frozen=True)
class SummaryConfig:
    money_format_mode: str
    int_format_mode: str
    currency_symbol: str
    calc_config: Sequence[tuple[str, str]]
    required_calcs: Sequence[str]
    summary_template: dict[str, object]
    summary_key_map: Mapping[str, str]
    summary_options: Sequence[str]
    category_overview_title: str
    income_expense_overview_title: str
    key_value_pair_label: str
    transactions_analyzed_key: str
    net_balance_label: str
    income_label: str
    expense_label: str
    filter_by_key_value_label: str
    invalid_transaction_type: str
    date_format: str
