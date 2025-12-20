from __future__ import annotations

import streamlit as st

from finance_ui.api import endpoints
from finance_ui.components import export_tools, history_view
from finance_ui.state import keys
from finance_ui.ui.messages import show_api_error


def render() -> None:
    save_id = st.session_state.get(keys.SELECTED_SAVE_ID)
    if not save_id:
        st.error("No save selected.")
        return

    from finance_ui.ui.layout import render_last_action_banner
    render_last_action_banner()

    st.markdown("## Advanced")

    tabs = st.tabs(["History", "Storage", "Export"])

    with tabs[0]:
        history_view.render(save_id)

    with tabs[1]:
        st.markdown("#### Storage")
        try:
            with st.spinner("Loading save metadata..."):
                meta = endpoints.get_save(save_id)
            st.write(meta)
        except Exception as e:
            show_api_error(e)

        st.caption("Backup listing / file paths depend on backend support. Placeholder for now.")

    with tabs[2]:
        export_tools.render_csv_export(save_id)
