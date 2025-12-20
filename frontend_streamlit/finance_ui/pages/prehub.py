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
            if st.button("Load", width="stretch"):
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

        if st.button("Create empty save", width="stretch"):
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
        if not saves:
            st.info("No saves available.")
        else:
            restore_ids = [s.get("save_id") for s in saves if s.get("save_id")]
            if not restore_ids:
                st.info("No saves available.")
            else:
                restore_save_id = st.selectbox(
                    "Select save",
                    restore_ids,
                    key="restore_save_select",
                )

                try:
                    with st.spinner("Loading backups..."):
                        backups = endpoints.list_backups(restore_save_id)
                except Exception as e:
                    show_api_error(e)
                    return

                if not backups:
                    st.info("No backups found for this save.")
                else:
                    backup_map = {
                        b.get("filename") or b.get("path") or "(unknown)": b
                        for b in backups
                    }
                    backup_label = st.selectbox(
                        "Select backup",
                        list(backup_map.keys()),
                        key="restore_backup_select",
                    )

                    confirm = st.checkbox(
                        "I understand this will overwrite the save",
                        value=False,
                        key="restore_confirm",
                    )

                    if st.button(
                        "Restore latest backup",
                        width="stretch",
                        disabled=not confirm,
                        key="btn_restore_latest",
                    ):
                        try:
                            with st.spinner("Restoring latest backup..."):
                                res = endpoints.restore_latest_backup(restore_save_id)
                            if res.get("ok") is True:
                                st.success(res.get("message", "Backup restored."))
                                actions.select_save(restore_save_id)
                                st.rerun()
                            else:
                                st.error(res.get("message", "Backup restore failed."))
                        except Exception as e:
                            show_api_error(e)

                    if st.button(
                        "Restore selected backup",
                        width="stretch",
                        disabled=not confirm,
                        key="btn_restore_selected",
                    ):
                        backup = backup_map.get(backup_label) or {}
                        path = backup.get("path")
                        try:
                            with st.spinner("Restoring backup..."):
                                res = endpoints.restore_backup_file(restore_save_id, path)
                            if res.get("ok") is True:
                                st.success(res.get("message", "Backup restored."))
                                actions.select_save(restore_save_id)
                                st.rerun()
                            else:
                                st.error(res.get("message", "Backup restore failed."))
                        except Exception as e:
                            show_api_error(e)
