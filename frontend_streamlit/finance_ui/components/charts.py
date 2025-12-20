from __future__ import annotations

from typing import Any

import pandas as pd
import plotly.express as px


def _norm_label(x: Any) -> str:
    s = ""
    if x is not None:
        try:
            s = str(x).strip()
        except Exception:
            s = ""
    if not s or s.lower() == "none":
        return "unknown"
    return s


def net_over_time(by_month: dict[str, dict[str, float]] | None):
    if not by_month:
        return None

    rows: list[dict[str, Any]] = []
    for month, data in by_month.items():
        rows.append(
            {
                "month": month,
                "net": float(data.get("net", 0.0)),
            }
        )

    df = pd.DataFrame(rows).sort_values("month")
    fig = px.line(df, x="month", y="net", title="Net over time")
    return fig


def income_vs_expense_over_time(by_month: dict[str, dict[str, float]] | None):
    if not by_month:
        return None

    rows: list[dict[str, Any]] = []
    for month, data in by_month.items():
        rows.append(
            {
                "month": month,
                "income": float(data.get("I", 0.0)),
                "expense": float(data.get("E", 0.0)),
            }
        )

    df = pd.DataFrame(rows).sort_values("month")
    fig = px.bar(df, x="month", y=["income", "expense"], barmode="group", title="Income vs Expense over time")
    return fig


def expense_by_category(by_category: dict[str, float] | None):
    if not by_category:
        return None

    rows: list[dict[str, Any]] = []
    for cat, signed in by_category.items():
        try:
            v = float(signed)
        except Exception:
            continue
        if v < 0:
            rows.append({"category": _norm_label(cat), "expense": abs(v)})

    if not rows:
        return None

    df = pd.DataFrame(rows).sort_values("expense", ascending=False)
    fig = px.bar(df, x="category", y="expense", title="Expense by category")
    return fig


def income_by_category(by_category: dict[str, float] | None):
    if not by_category:
        return None

    rows: list[dict[str, Any]] = []
    for cat, signed in by_category.items():
        try:
            v = float(signed)
        except Exception:
            continue
        if v > 0:
            rows.append({"category": _norm_label(cat), "income": v})

    if not rows:
        return None

    df = pd.DataFrame(rows).sort_values("income", ascending=False)
    fig = px.bar(df, x="category", y="income", title="Income by category")
    return fig


def top_merchants(transactions: list[dict[str, Any]], top_n: int = 10, tx_type: str = "E"):
    if not transactions:
        return None

    metric = "expense" if tx_type == "E" else "income"
    title = "Top merchants (expenses)" if tx_type == "E" else "Top merchants (income)"

    rows: list[dict[str, Any]] = []
    for tx in transactions:
        t = tx.get("type")
        if t != tx_type:
            continue

        name = _norm_label(tx.get("name"))
        try:
            amt = float(tx.get("amount", 0.0))
        except Exception:
            continue
        rows.append({"merchant": name, metric: abs(amt)})

    if not rows:
        return None

    df = pd.DataFrame(rows)
    df = df.groupby("merchant", as_index=False)[metric].sum()
    df = df.sort_values(metric, ascending=False).head(int(top_n))

    fig = px.bar(df, x="merchant", y=metric, title=title)
    return fig
