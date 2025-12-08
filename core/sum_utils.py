# summarize with input from user
from __future__ import annotations

from datetime import datetime
from typing import Dict, Iterable, List, Sequence, Tuple, Union

from config.calc_summary import (
    REQUIRED_CALCS,
    SUMMARY_TEMPLATE,
    SUMMARY_KEY_MAP,
    CATEGORY_OVERVIEW_TITLE,
    INCOME_EXPENSE_OVERVIEW_TITLE,
    KEY_VALUE_PAIR_LABEL,
    TRANSACTIONS_ANALYZED_KEY,
    NET_BALANCE_LABEL,
)
from config.schema import DATE_FORMAT
from config.text import SUMMARY_OPTIONS, INCOME, EXPENSE

from core.calc_utils import calc_util_func as c_funcs
from core.sort_utils import sort_util_func as s_funcs

def initvars():
    return SUMMARY_TEMPLATE.copy()

def _safe_net_balance(dataset):
    """Compute net balance but ignore transactions with invalid 'type' values."""
    cleaned = [t for t in dataset if t.get("type") in ("I", "E")]
    if not cleaned:
        return 0.0
    return c_funcs[2][1](cleaned)


def _apply_calcs(summary, dataset):
    for label, func, _ in c_funcs:
        if label not in REQUIRED_CALCS:
            continue
        result = func(dataset)
        mapped_key = SUMMARY_KEY_MAP.get(label, label)
        summary[mapped_key] = result
    return summary

def summary_alltime(filterby_key, filterby_value, save):
    summary = initvars()
    summary[KEY_VALUE_PAIR_LABEL] = SUMMARY_OPTIONS[0]
    return _apply_calcs(summary, save)

def summary_general_overview(filterby_key, filterby_value, save):
    summary = {}
    summary["Special1"] = CATEGORY_OVERVIEW_TITLE
    summary[TRANSACTIONS_ANALYZED_KEY] = len(save)

    total_categories = list(set(item["category"] for item in save))
    summary["Total Categories"] = len(total_categories)

    category_list = []

    for category in total_categories:
        _, func = s_funcs[0]  # filter_save
        percategory_dict = {}

        filtered_save = func("category", category, save)
        percategory_dict["category_name"] = category
        percategory_dict["count"] = c_funcs[3][1](filtered_save)
        percategory_dict["total"] = c_funcs[2][1](filtered_save)
        category_list.append(percategory_dict)

    category_list.sort(key=lambda cat: cat["total"], reverse=True)

    summary["Categories"] = category_list
    summary[NET_BALANCE_LABEL] = _safe_net_balance(save)

    return summary


def summary_income_expense_overview(filterby_key, filterby_value, save):
    summary = {}
    summary["Special2"] = INCOME_EXPENSE_OVERVIEW_TITLE
    summary[TRANSACTIONS_ANALYZED_KEY] = len(save)

    total_types = ["I", "E"]

    for t in total_types:
        _, func = s_funcs[0]  # filter_save
        percategory_dict = {}

        filtered_save = func("type", t, save)
        percategory_dict["count"] = len(filtered_save)
        percategory_dict["total"] = _safe_net_balance(filtered_save)

        if t == "I":
            summary[INCOME] = percategory_dict
        else:
            summary[EXPENSE] = percategory_dict

    summary[NET_BALANCE_LABEL] = _safe_net_balance(save)

    return summary


def sum_by_key_value_pair(filterby_key, filterby_value, save):
    summary = initvars()
    _, func = s_funcs[0]  # filter_save
    filtered_save = func(filterby_key, filterby_value, save)
    summary[KEY_VALUE_PAIR_LABEL] = f"{filterby_key}: {filterby_value}"
    return _apply_calcs(summary, filtered_save)

def summary_by_daterange(filterby_key, filterby_value, save):
    summary = initvars()
    start_date_str, end_date_str = filterby_value
    start_date = datetime.strptime(start_date_str, DATE_FORMAT)
    end_date = datetime.strptime(end_date_str, DATE_FORMAT)

    filtered_save = []
    for transaction in save:
        transaction_date = datetime.strptime(transaction["date"], DATE_FORMAT)
        if start_date <= transaction_date <= end_date:
            filtered_save.append(transaction)

    summary[KEY_VALUE_PAIR_LABEL] = f"From {start_date_str} to {end_date_str}"
    return _apply_calcs(summary, filtered_save)

    


# Sum_utils - imported by cli/cli.py

sum_util_func = [  # DO NOT CHANGE ORDER - ORDER CRITICAL FOR SUMMARY OPTIONS
    (SUMMARY_OPTIONS[0], summary_alltime),
    (SUMMARY_OPTIONS[1], summary_general_overview),
    (SUMMARY_OPTIONS[2], summary_income_expense_overview),
    (SUMMARY_OPTIONS[3], sum_by_key_value_pair),
    (SUMMARY_OPTIONS[4], sum_by_key_value_pair),
    (SUMMARY_OPTIONS[5], sum_by_key_value_pair),
    (SUMMARY_OPTIONS[6], summary_by_daterange),
    (SUMMARY_OPTIONS[7], summary_by_daterange),
]
