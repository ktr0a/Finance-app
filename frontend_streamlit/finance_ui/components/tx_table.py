from __future__ import annotations

from typing import Any

import pandas as pd
import streamlit as st

from finance_ui.state import keys
from finance_ui.utils.category import canon_category


def render(items: list[dict[str, Any]]) -> None:
    """
    Renders a table and updates st.session_state[keys.SELECTED_TX_ID].

    Uses Streamlit row selection if available; otherwise falls back to a selectbox.
    """
    if not items:
        st.info("No transactions found.")
        st.session_state[keys.SELECTED_TX_ID] = None
        return

    df = pd.DataFrame(items)
    if "category" in df.columns:
        df["category"] = df["category"].apply(canon_category)

    # Ensure consistent column order for display
    display_cols = [c for c in ["date", "name", "category", "type", "amount", "id"] if c in df.columns]
    df = df[display_cols]

    st.markdown("#### Transactions")
    selected_id: str | None = st.session_state.get(keys.SELECTED_TX_ID)

    # Attempt interactive selection (newer Streamlit)
    try:
        event = st.dataframe(
            df,
            hide_index=True,
            width="stretch",
            on_select="rerun",
            selection_mode="single-row",
        )
        # event.selection.rows gives selected row indices
        rows = getattr(getattr(event, "selection", None), "rows", None)
        if rows:
            row_idx = rows[0]
            try:
                selected_id = str(df.iloc[row_idx]["id"])
            except Exception:
                selected_id = None
    except Exception:
        # Fallback: select by ID
        ids = [str(x.get("id")) for x in items if x.get("id") is not None]
        label_map = {f"{x.get('date')} | {x.get('name')} | {x.get('amount')} ({x.get('id')})": str(x.get("id")) for x in items}
        labels = list(label_map.keys())
        chosen = st.selectbox("Select transaction", labels, index=0)
        selected_id = label_map[chosen] if chosen else None

    st.session_state[keys.SELECTED_TX_ID] = selected_id

    if selected_id:
        st.caption(f"Selected tx_id: {selected_id}")
