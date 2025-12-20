"""Core engine module (merged utils). Step 1 only."""

from __future__ import annotations

from .models import Result
from .ports import History, Repository
from .services.summary import SummaryService


# ===== Engine Facade (Phase 1) =====


class Engine:
    def __init__(
        self,
        repo: Repository,
        history: History | None = None,
        summary_service: SummaryService | None = None,
    ) -> None:
        self.repo = repo
        self.history = history
        self.summary_service = summary_service

    def _require_summary(self) -> SummaryService:
        if self.summary_service is None:
            raise NotImplementedError("Summary service not configured")
        return self.summary_service

    def _load_state_raw(self):
        return self.repo.load()

    def _extract_save(self, state):
        if isinstance(state, tuple) and len(state) == 2:
            return state[1]
        return state

    def _rebuild_state(self, old_state, new_save):
        return new_save

    def load_state(self) -> Result:
        try:
            state = self.repo.load()
            return Result(ok=True, data=state)
        except Exception as exc:
            return Result(ok=False, error=exc)

    def save_state(self, state) -> Result:
        try:
            self.repo.save(state)
            return Result(ok=True, data=True)
        except Exception as exc:
            return Result(ok=False, data=None, error=exc)

    def _prepare_mutation(self, save) -> Result:
        snap_res = self.push_undo_snapshot(save)
        if not snap_res.ok or snap_res.data is not True:
            return Result(ok=False, error=RuntimeError("undo snapshot failed"))

        self.clear_redo_stack()
        return Result(ok=True, data=True)

    def list_transactions(self) -> Result:
        try:
            state = self._load_state_raw()
            save = self._extract_save(state)
            if save is None:
                return Result(ok=False, error=ValueError("no save loaded"))
            return Result(ok=True, data=save)
        except Exception as exc:
            return Result(ok=False, error=exc)

    def add_transaction(self, tx: dict, *, snapshot: bool = True) -> Result:
        try:
            state = self._load_state_raw()
            save = self._extract_save(state)
            if save is None:
                return Result(ok=False, error=ValueError("no save loaded"))

            if snapshot:
                prep_res = self._prepare_mutation(save)
                if not prep_res.ok:
                    return prep_res

            save.append(tx)
            new_state = self._rebuild_state(state, save)
            self.repo.save(new_state)
            return Result(ok=True, data=save)
        except Exception as exc:
            return Result(ok=False, error=exc)

    def edit_transaction(
        self,
        index: int,
        patch: dict | None = None,
        new_tx: dict | None = None,
        *,
        snapshot: bool = True,
    ) -> Result:
        try:
            state = self._load_state_raw()
            save = self._extract_save(state)
            if save is None:
                return Result(ok=False, error=ValueError("no save loaded"))

            if not 0 <= index < len(save):
                return Result(ok=False, error=IndexError("transaction index out of range"))

            if snapshot:
                prep_res = self._prepare_mutation(save)
                if not prep_res.ok:
                    return prep_res

            if new_tx is not None:
                save[index] = new_tx
            elif patch is not None:
                save[index].update(patch)
            else:
                return Result(ok=False, error=TypeError("edit_transaction requires patch or new_tx"))

            new_state = self._rebuild_state(state, save)
            self.repo.save(new_state)
            return Result(ok=True, data=save)
        except Exception as exc:
            return Result(ok=False, error=exc)

    def delete_transaction(self, index: int, *, snapshot: bool = True) -> Result:
        try:
            state = self._load_state_raw()
            save = self._extract_save(state)
            if save is None:
                return Result(ok=False, error=ValueError("no save loaded"))

            if not 0 <= index < len(save):
                return Result(ok=False, error=IndexError("transaction index out of range"))

            if snapshot:
                prep_res = self._prepare_mutation(save)
                if not prep_res.ok:
                    return prep_res

            save.pop(index)
            new_state = self._rebuild_state(state, save)
            self.repo.save(new_state)
            return Result(ok=True, data=save)
        except Exception as exc:
            return Result(ok=False, error=exc)

    def import_transactions(self, txs: list[dict], *, snapshot: bool = True) -> Result:
        try:
            state = self._load_state_raw()
            save = self._extract_save(state)
            if save is None:
                return Result(ok=False, error=ValueError("no save loaded"))

            if not txs:
                return Result(ok=True, data=save)

            if snapshot:
                prep_res = self._prepare_mutation(save)
                if not prep_res.ok:
                    return prep_res

            save.extend(txs)
            new_state = self._rebuild_state(state, save)
            self.repo.save(new_state)
            return Result(ok=True, data=save)
        except Exception as exc:
            return Result(ok=False, error=exc)

    def summary(self, *args, **kwargs) -> Result:
        try:
            service = self._require_summary()
            return Result(ok=True, data=service.summary(*args, **kwargs))
        except Exception as exc:
            return Result(ok=False, error=exc)

    def undo(self, *args, **kwargs) -> Result:
        if self.history is None:
            return Result(
                ok=False,
                error=NotImplementedError("Phase 2: history not configured"),
            )

        try:
            state = self.history.undo()
            return Result(ok=True, data=state)
        except Exception as exc:
            return Result(ok=False, error=exc)

    def redo(self, *args, **kwargs) -> Result:
        if self.history is None:
            return Result(
                ok=False,
                error=NotImplementedError("Phase 2: history not configured"),
            )

        try:
            state = self.history.redo()
            return Result(ok=True, data=state)
        except Exception as exc:
            return Result(ok=False, error=exc)

    def filter_transactions(self, filterby_key, filterby_value, transactions) -> Result:
        try:
            service = self._require_summary()
            return Result(ok=True, data=service.filter_save(filterby_key, filterby_value, transactions))
        except Exception as exc:
            return Result(ok=False, error=exc)

    def calc_menu(self) -> Result:
        try:
            service = self._require_summary()
            return Result(ok=True, data=service.calc_menu())
        except Exception as exc:
            return Result(ok=False, error=exc)

    def run_calc(self, choice: int, transactions) -> Result:
        try:
            service = self._require_summary()
            return Result(ok=True, data=service.run_calc(choice, transactions))
        except Exception as exc:
            return Result(ok=False, error=exc)

    def format_value(self, value, mode: str) -> Result:
        try:
            service = self._require_summary()
            return Result(ok=True, data=service.format_value(value, mode))
        except Exception as exc:
            return Result(ok=False, error=exc)

    def summary_menu(self) -> Result:
        try:
            service = self._require_summary()
            return Result(ok=True, data=service.summary_menu())
        except Exception as exc:
            return Result(ok=False, error=exc)

    def summary_template(self) -> Result:
        try:
            service = self._require_summary()
            return Result(ok=True, data=service.summary_template())
        except Exception as exc:
            return Result(ok=False, error=exc)

    def create_backup(self, state) -> Result:
        try:
            if hasattr(self.repo, "create_backup"):
                status = self.repo.create_backup(state)  # type: ignore[attr-defined]
                return Result(ok=True, data=status)
            raise NotImplementedError("Backup not supported by repository")
        except Exception as exc:
            return Result(ok=False, error=exc)

    def list_backups(self) -> Result:
        try:
            if hasattr(self.repo, "list_backups"):
                backups = self.repo.list_backups()  # type: ignore[attr-defined]
                return Result(ok=True, data=backups)
            raise NotImplementedError("Backup listing not supported by repository")
        except Exception as exc:
            return Result(ok=False, error=exc)

    def restore_backup_file(self, path) -> Result:
        try:
            if hasattr(self.repo, "restore_backup_file"):
                status = self.repo.restore_backup_file(path)  # type: ignore[attr-defined]
                return Result(ok=True, data=status)
            raise NotImplementedError("Restore not supported by repository")
        except Exception as exc:
            return Result(ok=False, error=exc)

    def restore_latest_backup(self) -> Result:
        try:
            if hasattr(self.repo, "restore_latest_backup"):
                status = self.repo.restore_latest_backup()  # type: ignore[attr-defined]
                return Result(ok=True, data=status)
            raise NotImplementedError("Restore not supported by repository")
        except Exception as exc:
            return Result(ok=False, error=exc)

    def delete_backup_files(self, backups) -> Result:
        try:
            if hasattr(self.repo, "delete_backup_files"):
                status = self.repo.delete_backup_files(backups)  # type: ignore[attr-defined]
                return Result(ok=True, data=status)
            raise NotImplementedError("Backup cleanup not supported by repository")
        except Exception as exc:
            return Result(ok=False, error=exc)

    def push_undo_snapshot(self, state) -> Result:
        try:
            if hasattr(self.repo, "create_backup"):
                status = self.repo.create_backup(  # type: ignore[attr-defined]
                    state, mode="undo", delbackup=False
                )
                return Result(ok=True, data=status)
            raise NotImplementedError("Undo snapshot not supported by repository")
        except Exception as exc:
            return Result(ok=False, error=exc)

    def clear_undo_stack(self) -> Result:
        try:
            if hasattr(self.repo, "clear_undo_stack"):
                status = self.repo.clear_undo_stack()  # type: ignore[attr-defined]
                return Result(ok=True, data=status)
            raise NotImplementedError("Undo stack not supported by repository")
        except Exception as exc:
            return Result(ok=False, error=exc)

    def clear_redo_stack(self) -> Result:
        try:
            if hasattr(self.repo, "clear_redo_stack"):
                status = self.repo.clear_redo_stack()  # type: ignore[attr-defined]
                return Result(ok=True, data=status)
            raise NotImplementedError("Redo stack not supported by repository")
        except Exception as exc:
            return Result(ok=False, error=exc)

    def session_backup(self, state) -> Result:
        try:
            if hasattr(self.repo, "session_backup"):
                self.repo.session_backup()  # type: ignore[attr-defined]
            else:
                raise NotImplementedError("Session backup not supported by repository")

            return self.save_state(state)
        except Exception as exc:
            return Result(ok=False, error=exc)


