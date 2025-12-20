from __future__ import annotations

import streamlit as st

from finance_ui.api import endpoints
from finance_ui.state import actions, keys


PAGES = ["Transactions", "Summary", "Import", "Advanced", "Settings"]


@st.cache_data(ttl=5)
def _cached_health(base_url: str) -> bool:
    # base_url is included to ensure cache invalidates when URL changes
    return endpoints.health().get("ok") is True


def render() -> None:
    save_id = st.session_state.get(keys.SELECTED_SAVE_ID)

    with st.sidebar:
        st.markdown("### Current Save")
        st.write(save_id)

        if st.button("Change save"):
            actions.deselect_save()
            st.rerun()

        st.divider()

        st.markdown("### Navigation")
        current = st.session_state.get(keys.ACTIVE_PAGE, "Transactions")
        choice = st.radio("Go to", PAGES, index=PAGES.index(current) if current in PAGES else 0)
        st.session_state[keys.ACTIVE_PAGE] = choice

        st.divider()

        st.markdown("### Health")
        base_url = st.session_state.get(keys.API_BASE_URL, "")
        try:
            ok = _cached_health(base_url)
            st.success("API OK") if ok else st.error("API DOWN")
        except Exception:
            st.error("API DOWN")
