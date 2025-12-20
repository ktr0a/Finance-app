from __future__ import annotations

from datetime import date
from typing import Any

import streamlit as st

from finance_ui.api import endpoints
from finance_ui.state import keys
from finance_ui.ui.messages import show_api_error
from finance_ui.utils.dates import from_api_date, to_api_date


def _tx_type_label_to_api(v: str) -> str:
    return "I" if v == "Income" else "E"


def _tx_type_api_to_label(v: str) -> str:
    return "Income" if v == "I" else "Expense"


def _set_saved_msg() -> None:
    st.session_state[keys.LAST_ACTION_MSG] = "Saved ✓ You can Undo."
    # Force reload on next run
    st.session_state[keys.TX_CACHE] = {}


def render_add(save_id: str) -> None:
    with st.form("tx_add_form", clear_on_submit=False):
        name = st.text_input("Name", value="")
        category = st.text_input("Category", value="unknown")
        tlabel = st.selectbox("Type", ["Income", "Expense"], index=0)
        amount = st.number_input("Amount", value=0.0, step=0.01)
        d = st.date_input("Date", value=date.today())

        submitted = st.form_submit_button("Add")
        if not submitted:
            return

        tx = {
            "name": name.strip(),
            "category": category.strip() or "unknown",
            "type": _tx_type_label_to_api(tlabel),
            "amount": float(amount),
            "date": to_api_date(d),
        }

        try:
            with st.spinner("Saving..."):
                endpoints.add_transaction(save_id, tx)
            _set_saved_msg()
            st.rerun()
        except Exception as e:
            show_api_error(e)


def render_edit(save_id: str, selected_tx: dict[str, Any] | None) -> None:
    if not selected_tx:
        st.info("Select a transaction to edit.")
        return

    # Prefill
    default_date = date.today()
    try:
        default_date = from_api_date(str(selected_tx.get("date")))
    except Exception:
        pass

    with st.form("tx_edit_form", clear_on_submit=False):
        name = st.text_input("Name", value=str(selected_tx.get("name") or ""))
        category = st.text_input("Category", value=str(selected_tx.get("category") or "unknown"))
        tlabel = st.selectbox("Type", ["Income", "Expense"], index=0 if selected_tx.get("type") == "I" else 1)
        amount = st.number_input("Amount", value=float(selected_tx.get("amount") or 0.0), step=0.01)
        d = st.date_input("Date", value=default_date)

        submitted = st.form_submit_button("Update")
        if not submitted:
            return

        patch = {
            "name": name.strip(),
            "category": category.strip() or "unknown",
            "type": _tx_type_label_to_api(tlabel),
            "amount": float(amount),
            "date": to_api_date(d),
        }

        tx_id = str(selected_tx.get("id"))
        try:
            with st.spinner("Updating..."):
                endpoints.update_transaction(save_id, tx_id, patch)
            _set_saved_msg()
            st.rerun()
        except Exception as e:
            show_api_error(e)


def render_delete(save_id: str, selected_tx: dict[str, Any] | None) -> None:
    if not selected_tx:
        st.info("Select a transaction to delete.")
        return

    tx_id = str(selected_tx.get("id"))
    st.warning(f"Delete transaction {tx_id}?")

    confirm = st.checkbox("I understand this cannot be undone without Undo.", value=False)
    if not confirm:
        return

    if st.button("Delete", type="primary"):
        try:
            with st.spinner("Deleting..."):
                endpoints.delete_transaction(save_id, tx_id)
            _set_saved_msg()
            st.rerun()
        except Exception as e:
            show_api_error(e)
