from __future__ import annotations

from datetime import datetime
from pathlib import Path
import json
import re

from finance_app.api.errors import InvalidRequestError, SaveNotFoundError
from finance_app.api.schemas import SaveInfo
from finance_app.api.settings import SAVE_DIR, SAVE_FILE_NAME

_SAVE_ID_PATTERN = re.compile(r"^[A-Za-z0-9_-]+$")
_LEGACY_SAVE_ID = Path(SAVE_FILE_NAME).stem


def _validate_save_id(save_id: str) -> str:
    if not save_id:
        raise InvalidRequestError("save_id is required")
    if any(token in save_id for token in ("/", "\\", "..")):
        raise InvalidRequestError("save_id must not contain path separators or '..'")
    if not _SAVE_ID_PATTERN.fullmatch(save_id):
        raise InvalidRequestError("save_id must use letters, numbers, '_' or '-' only")
    return save_id


def _count_transactions(path: Path) -> int | None:
    try:
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, list):
            return len(data)
    except (OSError, json.JSONDecodeError, TypeError, ValueError):
        return None
    return None


def _save_info_from_path(save_id: str, path: Path) -> SaveInfo:
    updated_at = None
    try:
        updated_at = datetime.fromtimestamp(path.stat().st_mtime).isoformat()
    except OSError:
        updated_at = None

    tx_count = _count_transactions(path)

    return SaveInfo(
        save_id=save_id,
        filename=path.name,
        updated_at=updated_at,
        tx_count=tx_count,
    )


def list_saves() -> list[SaveInfo]:
    saves: list[SaveInfo] = []
    if not SAVE_DIR.exists():
        return saves

    legacy_path = SAVE_DIR / SAVE_FILE_NAME
    if legacy_path.exists():
        saves.append(_save_info_from_path(_LEGACY_SAVE_ID, legacy_path))

    for entry in SAVE_DIR.iterdir():
        if not entry.is_dir():
            continue

        save_file = entry / SAVE_FILE_NAME
        if not save_file.exists():
            continue

        save_id = entry.name
        if save_id == _LEGACY_SAVE_ID and legacy_path.exists():
            # Avoid duplicate IDs when legacy save.json exists.
            continue
        saves.append(_save_info_from_path(save_id, save_file))

    return saves


def resolve_save_path(save_id: str) -> Path:
    save_id = _validate_save_id(save_id)

    legacy_path = SAVE_DIR / SAVE_FILE_NAME
    dir_path = SAVE_DIR / save_id / SAVE_FILE_NAME

    if save_id == _LEGACY_SAVE_ID and legacy_path.exists():
        if dir_path.exists():
            raise InvalidRequestError("Ambiguous save_id 'save'")
        return legacy_path

    if not dir_path.exists():
        raise SaveNotFoundError(f"Save '{save_id}' not found")

    return dir_path


def create_save(name: str) -> SaveInfo:
    save_id = _validate_save_id(name)

    legacy_path = SAVE_DIR / SAVE_FILE_NAME
    if save_id == _LEGACY_SAVE_ID and legacy_path.exists():
        raise InvalidRequestError("save_id 'save' already exists")

    save_path = SAVE_DIR / save_id / SAVE_FILE_NAME
    if save_path.exists():
        raise InvalidRequestError(f"save_id '{save_id}' already exists")

    save_path.parent.mkdir(parents=True, exist_ok=True)
    save_path.write_text("[]", encoding="utf-8")

    return _save_info_from_path(save_id, save_path)


def get_save_info(save_id: str) -> SaveInfo:
    path = resolve_save_path(save_id)
    return _save_info_from_path(save_id, path)


def delete_save(save_id: str) -> bool:
    path = resolve_save_path(save_id)
    try:
        path.unlink()
    except OSError:
        return False

    legacy_path = SAVE_DIR / SAVE_FILE_NAME
    if path != legacy_path:
        try:
            path.parent.rmdir()
        except OSError:
            pass
    return True
