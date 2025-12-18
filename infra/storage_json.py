"""JSON storage implementation (Phase 3).

This module is a faithful port of `core/storage.py` into `infra/`, exposing
`Repository` + `History` implementations without changing formats or layout.
"""

from __future__ import annotations

import json
import shutil
from datetime import datetime as dt
from pathlib import Path

import core.core_config as core_config
from config.storage import (
    BACKUP_DIR_NAME,
    BACKUP_FILE_PREFIX,
    BACKUP_TIMESTAMP_FORMAT,
    DEFAULT_DATE,
    REDO_DIR_NAME,
    SAVE_FILENAME,
    STORAGE_DIR_NAME,
    UNDO_DIR_NAME,
)
from core.ports import History, Repository


class JsonRepository(Repository):
    def __init__(self, save_path: str = "storage/save.json"):
        self.save_path = Path(save_path)
        self.storage_dir = self.save_path.parent

        self.main_data_file = self.save_path
        self.backup_dir = self.storage_dir / BACKUP_DIR_NAME
        self.undo_dir = self.storage_dir / UNDO_DIR_NAME
        self.redo_dir = self.storage_dir / REDO_DIR_NAME

        self.backup_file_prefix = BACKUP_FILE_PREFIX
        self.backup_timestamp_format = BACKUP_TIMESTAMP_FORMAT

    def load(self) -> object:
        return self._load_like_core()

    def save(self, state: object) -> None:
        status = self._save_like_core(state)
        if status is not True:
            raise RuntimeError("JsonRepository.save failed")

    def _save_like_core(self, lst, *args):
        try:
            self.main_data_file.parent.mkdir(parents=True, exist_ok=True)
            with self.main_data_file.open("w", encoding="utf-8") as f:
                json.dump(lst, f, indent=4)
        except (OSError, TypeError, ValueError):
            return None  # failsafe
        return True

    def _load_like_core(self):
        if self.main_data_file.exists() is False:
            return None, None  # no save yet

        try:
            with self.main_data_file.open("r", encoding="utf-8") as f:
                data = json.load(f)
        except (OSError, json.JSONDecodeError, TypeError, ValueError):
            return None, None

        if not isinstance(data, list):
            return None, None

        for txn in data:
            if isinstance(txn, dict) and "date" not in txn:
                txn["date"] = DEFAULT_DATE

        if not data:
            return False, data

        return True, data  # returns status flag plus list of dicts

    def _cr_backup_json_like_core(self):
        if not self.main_data_file.exists():
            return False  # nothing to back up

        time_now = dt.now().strftime(self.backup_timestamp_format)
        backup_file = self.backup_dir / f"{self.backup_file_prefix}{time_now}.json"
        backup_file.parent.mkdir(parents=True, exist_ok=True)

        shutil.copy2(self.main_data_file, backup_file)

        self._del_backup_like_core()

        return True

    def _cr_backup_lst_like_core(self, lst, mode=None, delbackup=True):
        time_now = dt.now().strftime(self.backup_timestamp_format)

        if not mode:
            backup_file = self.backup_dir / f"{self.backup_file_prefix}{time_now}.json"
        elif mode == "undo":
            backup_file = self.undo_dir / f"{self.backup_file_prefix}{time_now}.json"
        elif mode == "redo":
            backup_file = self.redo_dir / f"{self.backup_file_prefix}{time_now}.json"
        else:
            raise SystemExit("invalid arg")

        backup_file.parent.mkdir(parents=True, exist_ok=True)

        try:
            with backup_file.open("w", encoding="utf-8") as f:
                json.dump(lst, f, indent=4)

            if mode is None and delbackup:
                self._del_backup_like_core()
        except (OSError, TypeError, ValueError):
            return None
        return True

    def _del_backup_like_core(self):
        backups = self._sort_backups_like_core(ascending=True)  # oldest -> newest

        if not backups:
            return None  # no backup folder or no backups

        backup_deleted = False

        while len(backups) > core_config.AMOUNT_OF_BACKUPS:
            oldest = backups.pop(0)  # oldest is always at index 0
            oldest.unlink()
            backup_deleted = True

        return backup_deleted

    def _sort_backups_like_core(self, ascending: bool):
        backup_dir = Path(self.backup_dir)

        if not backup_dir.exists():
            return []  # no backup folder

        backups = list(backup_dir.glob(f"{self.backup_file_prefix}*.json"))

        file_time_pairs = []

        for file in backups:
            mtime = file.stat().st_mtime
            file_time_pairs.append((file, mtime))

        file_time_pairs.sort(key=lambda pair: pair[1])

        if ascending is True:
            return [file for file, _ in file_time_pairs]

        file_time_pairs.reverse()
        return [file for file, _ in file_time_pairs]


class JsonHistory(History):
    def __init__(
        self,
        repo: JsonRepository,
        undo_dir: str = str(Path(STORAGE_DIR_NAME) / UNDO_DIR_NAME),
        redo_dir: str = str(Path(STORAGE_DIR_NAME) / REDO_DIR_NAME),
    ):
        self.repo = repo
        self.undo_dir = Path(undo_dir)
        self.redo_dir = Path(redo_dir)

        self.backup_file_prefix = BACKUP_FILE_PREFIX
        self.repo.undo_dir = self.undo_dir
        self.repo.redo_dir = self.redo_dir

    def undo(self) -> object:
        if not self.undo_dir.exists():
            return None, None

        entries = []
        for path in self.undo_dir.glob(f"{self.backup_file_prefix}*.json"):
            try:
                entries.append((path.stat().st_mtime, path))
            except OSError:
                continue

        if not entries:
            return None, None

        entries.sort(key=lambda item: item[0], reverse=True)
        newest_undo = entries[0][1]

        status, main_save = self.repo._load_like_core()
        if status is None:
            return None, None

        redo_backup_status = self.repo._cr_backup_lst_like_core(
            main_save if main_save is not None else [],
            mode="redo",
            delbackup=False,
        )
        if redo_backup_status is not True:
            return None, None

        try:
            with newest_undo.open("r", encoding="utf-8") as f:
                undo_data = json.load(f)
        except (OSError, json.JSONDecodeError, TypeError, ValueError):
            return None, None

        if self.repo._save_like_core(undo_data) is not True:
            return False, None

        try:
            newest_undo.unlink()
        except OSError:
            return False, None

        status, newsave = self.repo._load_like_core()
        if status is not True:
            return False, None
        return True, newsave

    def redo(self) -> object:
        if not self.redo_dir.exists():
            return None, None

        entries = []
        for path in self.redo_dir.glob(f"{self.backup_file_prefix}*.json"):
            try:
                entries.append((path.stat().st_mtime, path))
            except OSError:
                continue

        if not entries:
            return None, None

        entries.sort(key=lambda item: item[0], reverse=True)
        latest_redo = entries[0][1]

        status, main_save = self.repo._load_like_core()
        if status is None:
            return None, None

        undo_backup_status = self.repo._cr_backup_lst_like_core(
            main_save if main_save is not None else [],
            mode="undo",
            delbackup=False,
        )
        if undo_backup_status is not True:
            return None, None

        try:
            with latest_redo.open("r", encoding="utf-8") as f:
                redo_data = json.load(f)
        except (OSError, json.JSONDecodeError, TypeError, ValueError):
            return None, None

        if self.repo._save_like_core(redo_data) is not True:
            return False, None

        try:
            latest_redo.unlink()
        except OSError:
            return False, None

        status, newsave = self.repo._load_like_core()
        if status is not True:
            return False, None
        return True, newsave
