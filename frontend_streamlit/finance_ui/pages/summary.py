from __future__ import annotations

from typing import Any

import streamlit as st

from finance_ui.api import endpoints
from finance_ui.components import charts
from finance_ui.state import keys
from finance_ui.ui.messages import show_api_error


def render() -> None:
    save_id = st.session_state.get(keys.SELECTED_SAVE_ID)
    if not save_id:
        st.error("No save selected.")
        return

    st.markdown("## Summary")

    if st.button("Refresh"):
        st.rerun()

    # Fetch save info (tx_count) + summary
    try:
        with st.spinner("Loading summary..."):
            info = endpoints.get_save(save_id)
            summary = endpoints.get_summary(save_id)
    except Exception as e:
        show_api_error(e)
        return

    tx_count = info.get("tx_count")
    income_total = float(summary.get("income_total", 0.0))
    expense_total = float(summary.get("expense_total", 0.0))
    net_total = float(summary.get("net_total", 0.0))

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total income", f"{income_total:,.2f}")
    c2.metric("Total expense", f"{expense_total:,.2f}")
    c3.metric("Net", f"{net_total:,.2f}")
    c4.metric("Transaction count", str(tx_count) if tx_count is not None else "—")

    warnings = summary.get("warnings") or []
    if warnings:
        with st.expander("Warnings"):
            for w in warnings:
                st.write(f"- {w}")

    by_month = summary.get("by_month")
    by_category = summary.get("by_category")

    st.divider()

    # Charts section
    fig1 = charts.net_over_time(by_month)
    if fig1 is None:
        st.info("Not enough data for Net over time.")
    else:
        st.plotly_chart(fig1, width="stretch")

    fig2 = charts.income_vs_expense_over_time(by_month)
    if fig2 is None:
        st.info("Not enough data for Income vs Expense over time.")
    else:
        st.plotly_chart(fig2, width="stretch")

    fig3 = charts.expense_by_category(by_category)
    if fig3 is None:
        st.info("No expense category breakdown available.")
    else:
        st.plotly_chart(fig3, width="stretch")

    # Top merchants requires transactions list (derived plot)
    try:
        with st.spinner("Loading merchants..."):
            page = endpoints.list_transactions(save_id, {"limit": 10000, "offset": 0})
        items = page.get("items", []) if isinstance(page, dict) else []
    except Exception as e:
        show_api_error(e)
        return

    fig4 = charts.top_merchants(items, top_n=10)
    if fig4 is None:
        st.info("No expense transactions available for Top merchants.")
    else:
        st.plotly_chart(fig4, width="stretch")
