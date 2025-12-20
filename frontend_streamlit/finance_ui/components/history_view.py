from __future__ import annotations

from typing import Any

import streamlit as st

from finance_ui.api import endpoints
from finance_ui.state import keys
from finance_ui.ui.messages import show_api_error


def render(save_id: str) -> None:
    st.markdown("#### History")

    try:
        with st.spinner("Loading history..."):
            data = endpoints.history(save_id)
    except Exception as e:
        show_api_error(e)
        return

    # Minimal schema-agnostic display: show dict keys and any operations list if present
    if isinstance(data, dict):
        ops = data.get("items") or data.get("operations") or data.get("history") or None
        undo_av = data.get("undo_available")
        redo_av = data.get("redo_available")

        c1, c2 = st.columns(2)
        if c1.button("Undo", width="stretch", disabled=undo_av is False):
            try:
                endpoints.undo(save_id)
                st.session_state[keys.LAST_ACTION_MSG] = "Undone ✓"
                st.session_state[keys.TX_CACHE] = {}
                st.rerun()
            except Exception:
                st.warning("Undo not available.")

        if c2.button("Redo", width="stretch", disabled=redo_av is False):
            try:
                endpoints.redo(save_id)
                st.session_state[keys.LAST_ACTION_MSG] = "Redone ✓"
                st.session_state[keys.TX_CACHE] = {}
                st.rerun()
            except Exception:
                st.warning("Redo not available.")

        st.divider()

        if isinstance(ops, list) and ops:
            # Show as a simple table
            st.write(ops)
        else:
            st.caption("No detailed history list available from backend.")
            with st.expander("Raw history payload"):
                st.write(data)
    else:
        st.caption("Unexpected history response format.")
        with st.expander("Raw history payload"):
            st.write(data)
