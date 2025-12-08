# Calculations with list of items & parameters (dicts). Returns 
from config.calc_summary import (
    MONEY_FORMAT_MODE,
    INT_FORMAT_MODE,
    CURRENCY_SYMBOL,
    CALC_CONFIG,
)
from config.text import INVALID_TRANSACTION_TYPE


def format(value, mode: str) -> str:
    if mode == MONEY_FORMAT_MODE:
        return f"{value:.2f}{CURRENCY_SYMBOL}"
    if mode == INT_FORMAT_MODE:
        return str(value)
    return str(value)  # failsafe


def split_IE(transactions): # seperate i/e
    income = []
    expense = []
    for i in range(len(transactions)):
        if transactions[i]["type"] == "I":
            income.append(transactions[i])
        elif transactions[i]["type"] == "E":
            expense.append(transactions[i])
        else: 
            raise ValueError(
                INVALID_TRANSACTION_TYPE.format(
                    name=transactions[i]["name"],
                    type=transactions[i]["type"],
                )
            )
    return income, expense


def toti_raw(save) -> float:
    income, _ = split_IE(save)
    return sum(t["amount"] for t in income)


def tote_raw(save) -> float:
    _, expense = split_IE(save)
    return sum(t["amount"] for t in expense)


def netbal_raw(save) -> float:
    return toti_raw(save) - tote_raw(save)


def count_transactions(save) -> int:
    return len(save)


def avg_transaction_amount(save) -> float:
    if not save:
        return 0.0
    return sum(v["amount"] for v in save) / len(save)


def max_transaction_amount(save) -> float:
    if not save:
        return 0.0
    return max(v["amount"] for v in save)


def min_transaction_amount(save) -> float:
    if not save:
        return 0.0
    return min(v["amount"] for v in save)


CALC_FUNCTION_SEQUENCE = [
    toti_raw,
    tote_raw,
    netbal_raw,
    count_transactions,
    avg_transaction_amount,
    max_transaction_amount,
    min_transaction_amount,
]

CALC_FUNCTIONS = {
    label: func for (label, _), func in zip(CALC_CONFIG, CALC_FUNCTION_SEQUENCE)
}

# UTILS - imported by cli/cli.py
calc_util_func = [
    (label, CALC_FUNCTIONS[label], mode) for label, mode in CALC_CONFIG
]
