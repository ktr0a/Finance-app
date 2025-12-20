from __future__ import annotations

import streamlit as st

from finance_ui.api import endpoints
from finance_ui.state import actions, keys
from finance_ui.ui.messages import show_api_error


PAGES = ["Transactions", "Summary", "Import", "Advanced", "Settings"]


@st.cache_data(ttl=5)
def _cached_health(base_url: str) -> bool:
    # base_url is included to ensure cache invalidates when URL changes
    return endpoints.health().get("ok") is True


def render() -> None:
    save_id = st.session_state.get(keys.SELECTED_SAVE_ID)

    with st.sidebar:
        st.markdown("### Current Save")
        meta = None
        try:
            meta = endpoints.get_save(save_id) if save_id else None
        except Exception:
            meta = None

        if meta and isinstance(meta, dict):
            sid = meta.get("save_id") or save_id
            name = meta.get("filename") or meta.get("name")
            txc = meta.get("tx_count")

            st.write(f"**ID:** {sid}")
            if name:
                st.write(f"**Name:** {name}")
            if txc is not None:
                st.write(f"**Tx count:** {txc}")
        else:
            st.write(save_id)

        if st.button("Change save"):
            actions.deselect_save()
            st.rerun()

        st.markdown("### Danger zone")
        confirm_del = st.checkbox("I understand this deletes the save", value=False)
        if st.button("Delete save", type="primary", disabled=not confirm_del):
            try:
                endpoints.delete_save(save_id)
                actions.deselect_save()
                st.rerun()
            except Exception as e:
                show_api_error(e)

        st.divider()

        st.markdown("### Quick Actions")
        if st.button("Undo"):
            try:
                endpoints.undo(save_id)
                st.session_state[keys.LAST_ACTION_MSG] = "Undone ✓"
                st.session_state[keys.TX_CACHE] = {}
                st.rerun()
            except Exception:
                st.warning("Undo not available.")

        if st.button("Redo"):
            try:
                endpoints.redo(save_id)
                st.session_state[keys.LAST_ACTION_MSG] = "Redone ✓"
                st.session_state[keys.TX_CACHE] = {}
                st.rerun()
            except Exception:
                st.warning("Redo not available.")

        st.divider()

        st.markdown("### Navigation")
        current = st.session_state.get(keys.ACTIVE_PAGE, "Summary")
        st.radio(
            "Go to",
            PAGES,
            index=PAGES.index(current) if current in PAGES else 0,
            key=keys.ACTIVE_PAGE,  # stable widget key prevents “double click” / state drift
        )

        st.divider()

        st.markdown("### Health")
        base_url = st.session_state.get(keys.API_BASE_URL, "")
        try:
            ok = _cached_health(base_url)
            st.success("API OK") if ok else st.error("API DOWN")
        except Exception:
            st.error("API DOWN")

        st.divider()
        st.markdown("### Tools")
        base_url = st.session_state.get(keys.API_BASE_URL, "").rstrip("/")
        if base_url:
            st.link_button("Open API docs", f"{base_url}/docs", width="stretch")
