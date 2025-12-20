from __future__ import annotations

import streamlit as st

from finance_ui.state import keys


def _default_save_name() -> str:
    # Safe default, never empty. Format is frozen for UX but not required by backend.
    # Must match [A-Za-z0-9_-]+
    import datetime as _dt
    today = _dt.date.today().isoformat()  # YYYY-MM-DD
    return f"save_{today}"


def ensure_defaults() -> None:
    ss = st.session_state

    ss.setdefault(keys.API_BASE_URL, "http://127.0.0.1:8000")
    ss.setdefault(keys.SELECTED_SAVE_ID, None)
    ss.setdefault(keys.ACTIVE_PAGE, "Transactions")

    ss.setdefault(
        keys.TX_FILTERS,
        {
            "q": None,
            "type": None,
            "category": None,
            "date_from": None,
            "date_to": None,
            "sort": None,
            "order": None,
            "limit": 200,
            "offset": 0,
        },
    )
    ss.setdefault(keys.TX_CACHE, {})
    ss.setdefault(keys.PDF_PREVIEW, None)
    ss.setdefault(keys.LAST_ACTION_MSG, None)

    ss.setdefault(keys.IMPORT_STEP, 1)
    ss.setdefault(keys.SELECTED_TX_ID, None)

    # Prehub helper value (not part of required keys, but allowed as local UI state)
    ss.setdefault("prehub_new_save_name", _default_save_name())


def reset_ui_state() -> None:
    ss = st.session_state
    ss[keys.TX_CACHE] = {}
    ss[keys.PDF_PREVIEW] = None
    ss[keys.LAST_ACTION_MSG] = None
    ss[keys.IMPORT_STEP] = 1
    ss[keys.SELECTED_TX_ID] = None

    ss[keys.TX_FILTERS] = {
        "q": None,
        "type": None,
        "category": None,
        "date_from": None,
        "date_to": None,
        "sort": None,
        "order": None,
        "limit": 200,
        "offset": 0,
    }
