from __future__ import annotations

import streamlit as st

from finance_ui.api import endpoints
from finance_ui.state import actions, keys
from finance_ui.ui.messages import show_api_error


PAGES = ["Summary", "Transactions", "Import"]


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

        st.markdown("### Quick Actions")
        c1, c2 = st.columns(2)

        with c1:
            if st.button("Undo", use_container_width=True):
                try:
                    endpoints.undo(save_id)
                    st.session_state[keys.LAST_ACTION_MSG] = "Undone ✓"
                    st.session_state[keys.TX_CACHE] = {}
                    st.rerun()
                except Exception:
                    st.warning("Undo not available.")

        with c2:
            if st.button("Redo", use_container_width=True):
                try:
                    endpoints.redo(save_id)
                    st.session_state[keys.LAST_ACTION_MSG] = "Redone ✓"
                    st.session_state[keys.TX_CACHE] = {}
                    st.rerun()
                except Exception:
                    st.warning("Redo not available.")

        st.divider()

        st.markdown("### Navigation")
        ss = st.session_state

        current = ss.get(keys.ACTIVE_PAGE, "Summary")

        # Apply programmatic navigation request (safe: before widget instantiation)
        req = ss.get(keys.NAV_REQUESTED_PAGE)
        if req in PAGES:
            ss[keys.ACTIVE_PAGE_WIDGET] = req
            ss[keys.ACTIVE_PAGE] = req
            ss[keys.NAV_REQUESTED_PAGE] = None

        # Determine what the radio should show WITHOUT clobbering user clicks
        default = ss.get(keys.ACTIVE_PAGE_WIDGET)
        if default not in PAGES:
            default = current if current in PAGES else PAGES[0]
            ss[keys.ACTIVE_PAGE_WIDGET] = default  # safe: still before radio instantiation

        def _on_nav_change() -> None:
            picked = st.session_state.get(keys.ACTIVE_PAGE_WIDGET)
            if picked in PAGES:
                st.session_state[keys.ACTIVE_PAGE] = picked

        st.radio(
            "Go to",
            PAGES,
            index=PAGES.index(default),
            key=keys.ACTIVE_PAGE_WIDGET,
            on_change=_on_nav_change,
        )

        st.divider()

        with st.expander("Advanced", expanded=False):
            ss = st.session_state

            st.markdown("#### Pages")
            p1, p2 = st.columns(2)
            with p1:
                if st.button("Settings", use_container_width=True):
                    ss[keys.ACTIVE_PAGE] = "Settings"
                    st.rerun()
            with p2:
                if st.button("Advanced", use_container_width=True):
                    ss[keys.ACTIVE_PAGE] = "Advanced"
                    st.rerun()

            st.divider()

            st.markdown("#### Health")
            base_url = ss.get(keys.API_BASE_URL, "")
            try:
                ok = _cached_health(base_url)
                st.success("API OK") if ok else st.error("API DOWN")
            except Exception:
                st.error("API DOWN")

            st.divider()

            st.markdown("#### Tools")
            base_url = ss.get(keys.API_BASE_URL, "").rstrip("/")
            if base_url:
                st.link_button("Open API docs", f"{base_url}/docs", width="stretch")

            st.divider()

            st.markdown("#### Danger zone")
            confirm_del = st.checkbox(
                "I understand this deletes the save",
                value=False,
                key="danger_confirm_delete",
            )
            if st.button(
                "Delete save",
                type="primary",
                disabled=not confirm_del,
                use_container_width=True,
            ):
                try:
                    endpoints.delete_save(save_id)
                    actions.deselect_save()
                    st.rerun()
                except Exception as e:
                    show_api_error(e)
