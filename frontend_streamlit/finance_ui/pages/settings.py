from __future__ import annotations

import streamlit as st

from finance_ui.api import endpoints
from finance_ui.state import init as state_init, keys
from finance_ui.ui.messages import show_api_error


FRONTEND_VERSION = "0.1.0"


def render() -> None:
    st.markdown("## Settings")

    st.markdown("### API")
    base = st.text_input("API base URL", key=keys.API_BASE_URL)

    c1, c2 = st.columns(2)
    if c1.button("Test connection", width="stretch"):
        try:
            with st.spinner("Testing..."):
                out = endpoints.health()
            ok = isinstance(out, dict) and out.get("ok") is True
            if ok:
                st.success("Connected ✓")
            else:
                st.error("Health check failed.")
        except Exception as e:
            show_api_error(e)

    if c2.button("Clear UI cache/state", width="stretch"):
        state_init.reset_ui_state()
        st.success("UI state cleared.")
        st.rerun()

    st.divider()
    st.markdown("### Versions")
    st.write(f"Frontend: {FRONTEND_VERSION}")

    # show health status quietly (no exception stack)
    try:
        out = endpoints.health()
        st.write(f"Backend health: {'OK' if out.get('ok') is True else 'DOWN'}")
    except Exception:
        st.write("Backend health: DOWN")
