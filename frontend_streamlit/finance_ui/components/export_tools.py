from __future__ import annotations

from typing import Any

import streamlit as st

from finance_ui.api import endpoints
from finance_ui.ui.messages import show_api_error
from finance_ui.utils.csv_export import transactions_to_csv_bytes


def render_csv_export(save_id: str) -> None:
    st.markdown("#### Export")

    try:
        with st.spinner("Loading transactions for export..."):
            data = endpoints.list_transactions(save_id, {"limit": 100000, "offset": 0})
    except Exception as e:
        show_api_error(e)
        return

    items: list[dict[str, Any]] = []
    if isinstance(data, dict):
        items = data.get("items", []) or []

    if not items:
        st.info("No transactions to export.")
        return

    csv_bytes = transactions_to_csv_bytes(items)
    st.download_button(
        label="Download CSV",
        data=csv_bytes,
        file_name=f"{save_id}_transactions.csv",
        mime="text/csv",
        width="stretch",
    )
