from __future__ import annotations

from typing import Any

import streamlit as st

from finance_ui.api import endpoints
from finance_ui.components import charts
from finance_ui.state import keys
from finance_ui.ui.messages import show_api_error
from finance_ui.utils.filtering import clean_summary_filters


def render() -> None:
    save_id = st.session_state.get(keys.SELECTED_SAVE_ID)
    if not save_id:
        st.error("No save selected.")
        return

    st.markdown("## Summary")

    ss = st.session_state
    pinned = clean_summary_filters(ss.get(keys.SUMMARY_FILTERS, {}) or {})
    tx_live = clean_summary_filters(ss.get(keys.TX_FILTERS, {}) or {})

    use_tx = bool(ss.get(keys.SUMMARY_USE_TX_FILTERS, False))

    # If user has no pinned filter but *does* have a TX filter, auto-enable live mode once.
    # This matches the expected workflow: build filter in Transactions → go Summary → see filtered graphs.
    if not pinned and tx_live and not use_tx:
        ss[keys.SUMMARY_USE_TX_FILTERS] = True
        use_tx = True

    active_filter = tx_live if use_tx else pinned

    with st.expander("Filter (applies to all graphs)", expanded=bool(active_filter)):
        mode = "Transactions (live)" if use_tx else ("Pinned snapshot" if pinned else "None")
        st.write(f"**Mode:** {mode}")

        if use_tx:
            st.write("**Using Transactions filter:**", tx_live or {})
            c1, c2 = st.columns(2)
            with c1:
                if st.button("Pin current filter (snapshot)", use_container_width=True):
                    ss[keys.SUMMARY_FILTERS] = tx_live
                    ss[keys.SUMMARY_USE_TX_FILTERS] = False
                    st.rerun()
            with c2:
                if st.button("Disable filter in Summary", use_container_width=True):
                    ss[keys.SUMMARY_USE_TX_FILTERS] = False
                    st.rerun()

        else:
            if pinned:
                st.write("**Pinned filter:**", pinned)
                c1, c2 = st.columns(2)
                with c1:
                    if st.button("Clear pinned filter", use_container_width=True):
                        ss[keys.SUMMARY_FILTERS] = {}
                        st.rerun()
                with c2:
                    if st.button("Use Transactions filter instead", use_container_width=True):
                        ss[keys.SUMMARY_USE_TX_FILTERS] = True
                        st.rerun()
            else:
                st.info("No filter active. Create one in Transactions, then open Summary.")
                if tx_live:
                    if st.button("Use current Transactions filter", use_container_width=True):
                        ss[keys.SUMMARY_USE_TX_FILTERS] = True
                        st.rerun()
                if st.button("Edit filter in Transactions", use_container_width=True):
                    ss[keys.ACTIVE_PAGE] = "Transactions"
                    ss[keys.NAV_REQUESTED_PAGE] = "Transactions"
                    st.rerun()

    if st.button("Refresh"):
        st.rerun()

    # Fetch save info (tx_count) + summary
    try:
        with st.spinner("Loading summary..."):
            info = endpoints.get_save(save_id)
            summary = endpoints.get_summary(save_id, filters=active_filter)
    except Exception as e:
        show_api_error(e)
        return

    tx_count = info.get("tx_count")
    if active_filter:
        try:
            count_page = endpoints.list_transactions(save_id, {**active_filter, "limit": 1, "offset": 0})
            if isinstance(count_page, dict) and "total" in count_page:
                tx_count = count_page.get("total")
        except Exception:
            pass
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

    mode = st.radio(
        "Breakdown view",
        ["Expense", "Income"],
        horizontal=True,
        key="summary_breakdown_mode",
    )

    if mode == "Expense":
        fig3 = charts.expense_by_category(by_category)
        if fig3 is None:
            st.info("No expense category breakdown available.")
        else:
            st.plotly_chart(fig3, width="stretch")
    else:
        fig3 = charts.income_by_category(by_category)
        if fig3 is None:
            st.info("No income category breakdown available.")
        else:
            st.plotly_chart(fig3, width="stretch")

    # Top merchants requires transactions list (derived plot)
    try:
        with st.spinner("Loading merchants..."):
            page = endpoints.list_transactions(save_id, {**active_filter, "limit": 0, "offset": 0})
        items = page.get("items", []) if isinstance(page, dict) else []
        total = page.get("total", len(items)) if isinstance(page, dict) else len(items)
        if total and len(items) < int(total):
            st.warning("Top merchants uses a partial transaction list (limit). Consider increasing limit.")
    except Exception as e:
        show_api_error(e)
        return

    tx_type = "E" if mode == "Expense" else "I"
    fig4 = charts.top_merchants(items, top_n=10, tx_type=tx_type)
    if fig4 is None:
        if mode == "Expense":
            st.info("No expense transactions available for Top merchants.")
        else:
            st.info("No income transactions available for Top merchants.")
    else:
        st.plotly_chart(fig4, width="stretch")
