from __future__ import annotations

import streamlit as st

from finance_ui.utils.http import ApiError


def show_api_error(err: Exception) -> None:
    st.error("Backend request failed. Is FastAPI running?")
    with st.expander("Details"):
        if isinstance(err, ApiError):
            st.write(str(err))
            st.write(err.detail)
        else:
            st.exception(err)
