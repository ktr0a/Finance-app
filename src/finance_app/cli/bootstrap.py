from __future__ import annotations

from finance_app.cli.ui import params as ui_params
from finance_app.cli.ui import text as ui_text
from finance_app.core.schema import DATE_FORMAT
from finance_app.core.services.summary import SummaryService
from finance_app.core.services.summary_config import SummaryConfig
from finance_app.infra.engine_factory import build_engine_json


def build_cli_engine():
    summary_config = SummaryConfig(
        money_format_mode=ui_params.MONEY_FORMAT_MODE,
        int_format_mode=ui_params.INT_FORMAT_MODE,
        currency_symbol=ui_params.CURRENCY_SYMBOL,
        calc_config=ui_text.CALC_CONFIG,
        required_calcs=ui_text.REQUIRED_CALCS,
        summary_template=ui_text.SUMMARY_TEMPLATE,
        summary_key_map=ui_text.SUMMARY_KEY_MAP,
        summary_options=ui_text.SUMMARY_OPTIONS,
        category_overview_title=ui_text.CATEGORY_OVERVIEW_TITLE,
        income_expense_overview_title=ui_text.INCOME_EXPENSE_OVERVIEW_TITLE,
        key_value_pair_label=ui_text.KEY_VALUE_PAIR_LABEL,
        transactions_analyzed_key=ui_text.TRANSACTIONS_ANALYZED_KEY,
        net_balance_label=ui_text.NET_BALANCE_LABEL,
        income_label=ui_text.INCOME,
        expense_label=ui_text.EXPENSE,
        filter_by_key_value_label=ui_text.FILTER_BY_KEY_VALUE_LABEL,
        invalid_transaction_type=ui_text.INVALID_TRANSACTION_TYPE,
        date_format=DATE_FORMAT,
    )
    summary_service = SummaryService(summary_config)
    return build_engine_json(summary_service=summary_service)
