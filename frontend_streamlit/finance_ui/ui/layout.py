from __future__ import annotations

# Reserved for shared layout helpers (wide containers, page headers, etc.).
# Step 1 placeholder by spec. No logic yet.

import streamlit as st

from finance_ui.state import keys


def render_last_action_banner() -> None:
    msg = st.session_state.get(keys.LAST_ACTION_MSG)
    if msg:
        st.success(msg)
