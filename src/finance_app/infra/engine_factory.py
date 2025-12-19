from __future__ import annotations

from finance_app.core.engine import Engine
from finance_app.core.services.summary import SummaryService
from finance_app.config.storage import REDO_DIR_NAME, UNDO_DIR_NAME
from finance_app.infra.storage_json import JsonHistory, JsonRepository


def build_engine_json(
    *,
    save_path: str = "storage/save.json",
    summary_service: SummaryService | None = None,
) -> Engine:
    repo = JsonRepository(save_path=save_path)
    history = JsonHistory(
        repo=repo,
        undo_dir=str(repo.storage_dir / UNDO_DIR_NAME),
        redo_dir=str(repo.storage_dir / REDO_DIR_NAME),
    )
    return Engine(repo=repo, history=history, summary_service=summary_service)
