from __future__ import annotations

import tempfile
from pathlib import Path

from finance_app.infra.storage_json import JsonHistory, JsonRepository


def _assert(cond: bool, msg: str) -> None:
    if not cond:
        raise SystemExit(f"[FAIL] {msg}")


def main() -> None:
    with tempfile.TemporaryDirectory() as td:
        base = Path(td)
        save_path = base / "storage" / "save.json"

        # 1) Missing save file must be "no save detected", not "corrupted"
        repo = JsonRepository(save_path=str(save_path))
        state = repo.load()
        _assert(isinstance(state, tuple) and len(state) == 2, "repo.load must return (status, save)")
        status, save = state
        _assert(status is False, "missing save file must return status False")
        _assert(save == [], "missing save file must return empty list save")

        # 2) Undo must succeed even if resulting save becomes empty list
        history = JsonHistory(
            repo=repo,
            undo_dir=str(save_path.parent / "undo_stack"),
            redo_dir=str(save_path.parent / "redo_stack"),
        )

        # Start from empty save
        repo.save([])
        # Simulate engine snapshot before adding first tx: undo snapshot is empty list
        repo.create_backup([], mode="undo", delbackup=False)

        tx = {"name": "t", "category": "c", "type": "I", "amount": 1.0, "date": "01.01.2000"}
        repo.save([tx])

        u_status, u_save = history.undo()
        _assert(u_status is True, "undo should report success True")
        _assert(u_save == [], "undo should return empty list when reverting first add")

        r_status, r_save = history.redo()
        _assert(r_status is True, "redo should report success True")
        _assert(r_save == [tx], "redo should restore the transaction list")

    print("[OK] freeze regression checks passed")


if __name__ == "__main__":
    main()
