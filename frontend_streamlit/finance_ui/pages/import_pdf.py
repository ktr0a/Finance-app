from __future__ import annotations

import streamlit as st

from finance_ui.components import import_wizard
from finance_ui.state import keys


def render() -> None:
    save_id = st.session_state.get(keys.SELECTED_SAVE_ID)
    if not save_id:
        st.error("No save selected.")
        return

    from finance_ui.ui.layout import render_last_action_banner
    render_last_action_banner()

    import_wizard.render(save_id)
