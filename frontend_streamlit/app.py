from __future__ import annotations

import streamlit as st

from finance_ui.pages import prehub, transactions, summary, import_pdf, advanced, settings
from finance_ui.state import init as state_init, keys
from finance_ui.ui import sidebar


def main() -> None:
    st.set_page_config(page_title="Finance App", layout="wide")
    state_init.ensure_defaults()

    if st.session_state.get(keys.SELECTED_SAVE_ID) is None:
        prehub.render()
        return

    sidebar.render()

    page = st.session_state.get(keys.ACTIVE_PAGE, "Summary")
    if page == "Transactions":
        transactions.render()
    elif page == "Summary":
        summary.render()
    elif page == "Import":
        import_pdf.render()
    elif page == "Advanced":
        advanced.render()
    elif page == "Settings":
        settings.render()
    else:
        summary.render()


if __name__ == "__main__":
    main()
