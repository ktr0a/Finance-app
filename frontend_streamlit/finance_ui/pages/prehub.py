from __future__ import annotations

import streamlit as st

from finance_ui.api import endpoints
from finance_ui.state import actions
from finance_ui.ui.messages import show_api_error
from finance_ui.utils.validate import is_valid_save_id


def render() -> None:
    st.markdown("## Welcome / Prehub")

    try:
        with st.spinner("Loading saves..."):
            saves = endpoints.list_saves()
    except Exception as e:
        show_api_error(e)
        return

    col = st.columns([1, 2, 1])[1]
    with col:
        st.markdown("### Load existing save")
        if not saves:
            st.info("No saves found.")
        else:
            options = {f"{s.get('filename', s.get('save_id'))} ({s.get('save_id')})": s.get("save_id") for s in saves}
            label = st.selectbox("Select save", list(options.keys()), key="prehub_save_select")
            if st.button("Load", use_container_width=True):
                save_id = options[label]
                if save_id:
                    actions.select_save(save_id)
                    st.rerun()

        st.divider()

        st.markdown("### Create new save")
        name = st.text_input(
            "Save ID",
            key="prehub_new_save_name",
            help="Allowed: A–Z a–z 0–9 _ -",
        )

        if st.button("Create empty save", use_container_width=True):
            if not is_valid_save_id(name):
                st.error("Save ID must match: A–Z a–z 0–9 _ -")
            else:
                try:
                    with st.spinner("Creating save..."):
                        created = endpoints.create_save(name=name.strip())
                    save_id = created.get("save_id")
                    if save_id:
                        actions.select_save(save_id)
                        st.rerun()
                    st.error("Backend did not return a save_id.")
                except Exception as e:
                    show_api_error(e)

        st.divider()

        st.markdown("### Restore from backup")
        st.caption("Not implemented yet")
