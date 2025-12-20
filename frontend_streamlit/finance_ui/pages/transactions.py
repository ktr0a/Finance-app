from __future__ import annotations

from typing import Any

import streamlit as st

from finance_ui.api import endpoints
from finance_ui.components import tx_filters, tx_forms, tx_table
from finance_ui.state import keys
from finance_ui.ui.messages import show_api_error


def _load_transactions(save_id: str, filters: dict[str, Any]) -> dict[str, Any]:
    """
    Cached in st.session_state[keys.TX_CACHE] using exact filters dict.
    """
    cache = st.session_state.get(keys.TX_CACHE) or {}
    if cache.get("save_id") == save_id and cache.get("filters") == filters and "data" in cache:
        return cache["data"]

    data = endpoints.list_transactions(save_id, filters)
    st.session_state[keys.TX_CACHE] = {"save_id": save_id, "filters": dict(filters), "data": data}
    return data


def render() -> None:
    save_id = st.session_state.get(keys.SELECTED_SAVE_ID)
    if not save_id:
        st.error("No save selected.")
        return

    st.markdown("## Transactions")

    # Last action message + Undo button (frozen pattern)
    msg = st.session_state.get(keys.LAST_ACTION_MSG)
    if msg:
        st.success(msg)
        if st.button("Undo this change"):
            try:
                with st.spinner("Undoing..."):
                    endpoints.undo(save_id)
                st.session_state[keys.LAST_ACTION_MSG] = "Undone ✓"
                st.session_state[keys.TX_CACHE] = {}
                st.rerun()
            except Exception as e:
                show_api_error(e)

    # Load once (needed to derive categories)
    try:
        with st.spinner("Loading transactions..."):
            first = _load_transactions(save_id, st.session_state.get(keys.TX_FILTERS, {}))
    except Exception as e:
        show_api_error(e)
        return

    items = first.get("items", []) if isinstance(first, dict) else []
    total = first.get("total", 0) if isinstance(first, dict) else 0
    limit = first.get("limit", 0) if isinstance(first, dict) else 0
    offset = first.get("offset", 0) if isinstance(first, dict) else 0

    # Derive categories from current list (spec)
    categories_set = {str(x.get("category") or "").strip() for x in items if x.get("category") is not None}
    categories_set.add("unknown")
    categories = sorted({c for c in categories_set if c})

    # Filters
    filters = tx_filters.render(categories=categories)

    st.divider()
    st.markdown("### Summary")
    ss = st.session_state

    def _clean_for_summary(f: dict[str, Any]) -> dict[str, Any]:
        # Only keep keys the summary endpoint supports
        keep = ["q", "type", "category", "date_from", "date_to"]
        out: dict[str, Any] = {}
        for k in keep:
            v = f.get(k)
            if v is not None:
                out[k] = v
        return out

    if st.button("View Summary with this filter", use_container_width=True):
        ss[keys.SUMMARY_FILTERS] = _clean_for_summary(filters)
        ss[keys.ACTIVE_PAGE] = "Summary"
        ss[keys.NAV_REQUESTED_PAGE] = "Summary"
        st.rerun()

    # Reload if filters changed (tx_cache logic handles this)
    try:
        with st.spinner("Loading transactions..."):
            data = _load_transactions(save_id, filters)
    except Exception as e:
        show_api_error(e)
        return

    items = data.get("items", []) if isinstance(data, dict) else []
    total = data.get("total", 0) if isinstance(data, dict) else 0
    limit = data.get("limit", 0) if isinstance(data, dict) else 0
    offset = data.get("offset", 0) if isinstance(data, dict) else 0

    st.caption(f"Showing {len(items)} of {total} (limit={limit}, offset={offset})")

    if st.button("Refresh"):
        st.session_state[keys.TX_CACHE] = {}
        st.rerun()

    # Table + selection
    tx_table.render(items)

    selected_id = st.session_state.get(keys.SELECTED_TX_ID)
    selected_tx: dict[str, Any] | None = None
    if selected_id:
        for x in items:
            if str(x.get("id")) == str(selected_id):
                selected_tx = x
                break

    st.divider()
    tabs = st.tabs(["Add", "Edit", "Delete"])
    with tabs[0]:
        tx_forms.render_add(save_id)
    with tabs[1]:
        tx_forms.render_edit(save_id, selected_tx)
    with tabs[2]:
        tx_forms.render_delete(save_id, selected_tx)
