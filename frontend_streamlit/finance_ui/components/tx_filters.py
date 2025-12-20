from __future__ import annotations

from datetime import date
from typing import Any

import streamlit as st

from finance_ui.state import keys
from finance_ui.utils.category import canon_category
from finance_ui.utils.dates import from_api_date, to_api_date


def _normalize_none(s: str | None) -> str | None:
    if s is None:
        return None
    s = s.strip()
    return s or None


def _type_to_label(t: str | None) -> str:
    if t == "I":
        return "Income"
    if t == "E":
        return "Expense"
    return "All"


def _label_to_type(label: str) -> str | None:
    if label == "Income":
        return "I"
    if label == "Expense":
        return "E"
    return None


def render(categories: list[str]) -> dict[str, Any]:
    """
    Renders filter UI and updates st.session_state[keys.TX_FILTERS].

    Rule: changing any filter (except offset itself) resets offset=0.
    """
    ss = st.session_state
    f = dict(ss.get(keys.TX_FILTERS, {}))

    prev = f.copy()

    st.markdown("#### Filters")

    q = st.text_input("Search", value=f.get("q") or "")
    q = _normalize_none(q)

    type_options = ["All", "Income", "Expense"]
    desired_type_label = _type_to_label(f.get("type"))

    # Only fix invalid widget value; do NOT force-sync every run (it cancels user selection).
    if ss.get(keys.TX_TYPE_WIDGET) not in type_options:
        ss[keys.TX_TYPE_WIDGET] = desired_type_label if desired_type_label in type_options else "All"

    # Use index as a fallback only; actual value comes from widget state.
    current_type_label = ss.get(keys.TX_TYPE_WIDGET, desired_type_label)
    if current_type_label not in type_options:
        current_type_label = desired_type_label if desired_type_label in type_options else "All"

    type_label = st.selectbox(
        "Type",
        type_options,
        index=type_options.index(current_type_label),
        key=keys.TX_TYPE_WIDGET,
    )
    t = _label_to_type(type_label)

    # Build canonical category options (stable, no duplicates from casing/whitespace)
    canon_set = {canon_category(c) for c in categories if c}
    canon_set.add("unknown")

    # Stored category from TX_FILTERS (may be old on rerun)
    stored_cat = f.get("category")
    stored_cat_canon = canon_category(stored_cat) if stored_cat is not None else None
    if stored_cat_canon:
        canon_set.add(stored_cat_canon)

    # IMPORTANT: include current widget selection so it never "disappears" during reruns
    current_widget_cat = ss.get(keys.TX_CATEGORY_WIDGET)
    if isinstance(current_widget_cat, str) and current_widget_cat != "All":
        canon_set.add(canon_category(current_widget_cat))

    cat_options = ["All"] + sorted(canon_set)

    # Determine preferred default (only used if widget is invalid)
    desired_cat_label = "All" if stored_cat_canon is None else stored_cat_canon
    if desired_cat_label not in cat_options:
        desired_cat_label = "All"

    # Only fix invalid widget value; do NOT force-sync every run (it cancels user selection)
    if ss.get(keys.TX_CATEGORY_WIDGET) not in cat_options:
        ss[keys.TX_CATEGORY_WIDGET] = desired_cat_label

    current_cat_label = ss.get(keys.TX_CATEGORY_WIDGET, desired_cat_label)
    if current_cat_label not in cat_options:
        current_cat_label = desired_cat_label

    cat_label = st.selectbox(
        "Category",
        cat_options,
        index=cat_options.index(current_cat_label),
        key=keys.TX_CATEGORY_WIDGET,
    )
    category = None if cat_label == "All" else cat_label  # already canonical

    # Optional date range: Streamlit date_input cannot be empty, so we gate with a checkbox.
    existing_from = f.get("date_from")
    existing_to = f.get("date_to")
    use_date = st.checkbox(
        "Enable date range",
        value=bool(existing_from or existing_to),
        key="tx_use_date_range",
    )

    # Defaults: if existing values are present, parse them; otherwise today.
    from_default = date.today()
    to_default = date.today()
    if isinstance(existing_from, str):
        try:
            from_default = from_api_date(existing_from)
        except Exception:
            pass
    if isinstance(existing_to, str):
        try:
            to_default = from_api_date(existing_to)
        except Exception:
            pass

    c1, c2 = st.columns(2)
    d0 = c1.date_input("From", value=from_default, key="tx_date_from_input")
    d1 = c2.date_input("To", value=to_default, key="tx_date_to_input")

    date_from: str | None = None
    date_to: str | None = None
    if use_date:
        date_from = to_api_date(d0)
        date_to = to_api_date(d1)

    sort_label = st.selectbox("Sort", ["(none)", "date", "amount", "name", "category"], index=0)
    sort = None if sort_label == "(none)" else sort_label

    order_label = st.selectbox("Order", ["(none)", "asc", "desc"], index=0)
    order = None if order_label == "(none)" else order_label

    limit = st.selectbox("Limit", [50, 100, 200, 500], index=[50, 100, 200, 500].index(int(f.get("limit") or 200)))
    offset = st.number_input("Offset", min_value=0, step=1, value=int(f.get("offset") or 0))

    f.update(
        {
            "q": q,
            "type": t,
            "category": category,
            "date_from": date_from,
            "date_to": date_to,
            "sort": sort,
            "order": order,
            "limit": int(limit),
            "offset": int(offset),
        }
    )

    # Reset offset when any non-offset filter changes
    non_offset_keys = ["q", "type", "category", "date_from", "date_to", "sort", "order", "limit"]
    changed_non_offset = any(prev.get(k) != f.get(k) for k in non_offset_keys)
    if changed_non_offset and prev.get("offset") == f.get("offset"):
        f["offset"] = 0

    ss[keys.TX_FILTERS] = f
    return f
