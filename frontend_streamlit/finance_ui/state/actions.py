from __future__ import annotations

import streamlit as st

from finance_ui.state import keys, init as state_init


def select_save(save_id: str) -> None:
    st.session_state[keys.SELECTED_SAVE_ID] = save_id
    st.session_state[keys.ACTIVE_PAGE] = "Summary"
    state_init.reset_ui_state()
    st.session_state[keys.PDF_PREVIEW] = None
    st.session_state[keys.IMPORT_STEP] = 1
    if "pdf_preview_table" in st.session_state:
        del st.session_state["pdf_preview_table"]


def deselect_save() -> None:
    st.session_state[keys.SELECTED_SAVE_ID] = None
    st.session_state[keys.ACTIVE_PAGE] = "Transactions"
    state_init.reset_ui_state()
    st.session_state[keys.PDF_PREVIEW] = None
    st.session_state[keys.IMPORT_STEP] = 1
    if "pdf_preview_table" in st.session_state:
        del st.session_state["pdf_preview_table"]
