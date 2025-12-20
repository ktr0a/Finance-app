from __future__ import annotations

from finance_app.core.engine import Engine
from finance_app.core.services.summary import SummaryService
from finance_app.infra.storage_legacy import (
    cr_backup_json,
    cr_backup_lst,
    clear_undo_stack,
    clear_redo_stack,
    list_backups,
    restore_backup_file,
    restore_latest_backup,
    save,
    load,
    undo_action,
    redo_action,
)


class LegacyRepository:
    def load(self) -> object:
        return load()

    def save(self, state: object) -> None:
        status = save(state)
        if status is not True:
            raise RuntimeError("LegacyRepository.save failed")

    def _cr_backup_json_like_core(self):
        return cr_backup_json()

    def _cr_backup_lst_like_core(self, lst, mode=None, delbackup=True):
        return cr_backup_lst(lst, mode=mode, delbackup=delbackup)

    def create_backup(self, lst, mode=None, delbackup=True):
        return self._cr_backup_lst_like_core(lst, mode=mode, delbackup=delbackup)

    def session_backup(self):
        return self._cr_backup_json_like_core()

    def list_backups(self):
        return list_backups()

    def restore_backup_file(self, path):
        return restore_backup_file(path)

    def restore_latest_backup(self):
        return restore_latest_backup()

    def delete_backup_files(self, backups):
        cleanup_error = False
        for backup in backups:
            try:
                if not backup.exists():
                    continue
                backup.unlink()
            except OSError:
                cleanup_error = True
        return cleanup_error

    def clear_undo_stack(self) -> bool:
        clear_undo_stack()
        return True

    def clear_redo_stack(self) -> bool:
        clear_redo_stack()
        return True


class LegacyHistory:
    def undo(self) -> object:
        return undo_action()

    def redo(self) -> object:
        return redo_action()


def build_engine_legacy(summary_service: SummaryService | None = None) -> Engine:
    repo = LegacyRepository()
    history = LegacyHistory()
    return Engine(repo=repo, history=history, summary_service=summary_service)
