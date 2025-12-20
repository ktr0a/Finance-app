from __future__ import annotations

from typing import Any

from finance_ui.api.client import ApiClient


_client = ApiClient()


def health() -> dict:
    return _client.get("/health")


def list_saves() -> list[dict]:
    return _client.get("/saves")


def create_save(name: str) -> dict:
    return _client.post("/saves", json={"name": name})


def get_save(save_id: str) -> dict:
    return _client.get(f"/saves/{save_id}")


def delete_save(save_id: str) -> dict:
    return _client.delete(f"/saves/{save_id}")


def list_backups(save_id: str) -> list[dict]:
    return _client.get(f"/saves/{save_id}/backups")


def restore_latest_backup(save_id: str) -> dict:
    return _client.post(f"/saves/{save_id}/backups/restore-latest")


def restore_backup_file(save_id: str, path: str) -> dict:
    return _client.post(f"/saves/{save_id}/backups/restore", json={"path": path})


def list_transactions(save_id: str, filters: dict[str, Any]) -> dict:
    params = {k: v for k, v in filters.items() if v is not None}
    return _client.get(f"/saves/{save_id}/transactions", params=params)


def add_transaction(save_id: str, tx: dict) -> dict:
    return _client.post(f"/saves/{save_id}/transactions", json=tx)


def update_transaction(save_id: str, tx_id: str, patch: dict) -> dict:
    return _client.put(f"/saves/{save_id}/transactions/{tx_id}", json=patch)


def delete_transaction(save_id: str, tx_id: str) -> dict:
    return _client.delete(f"/saves/{save_id}/transactions/{tx_id}")


def get_summary(save_id: str) -> dict:
    return _client.get(f"/saves/{save_id}/summary")


def undo(save_id: str) -> dict:
    return _client.post(f"/saves/{save_id}/undo")


def redo(save_id: str) -> dict:
    return _client.post(f"/saves/{save_id}/redo")


def history(save_id: str) -> dict:
    return _client.get(f"/saves/{save_id}/history")


def pdf_parsers() -> dict:
    return _client.get("/pdf/parsers")


def pdf_preview(file_bytes: bytes, filename: str, parser: str | None = None, year: str | None = None) -> dict:
    files = {"file": (filename, file_bytes, "application/pdf")}
    data: dict[str, Any] = {}
    if parser:
        data["parser"] = parser
    if year:
        data["year"] = year
    return _client.post("/pdf/preview", files=files, data=data)


def pdf_apply(save_id: str, accepted: list[dict], source: str | None = None) -> dict:
    payload: dict[str, Any] = {"accepted": accepted, "source": source}
    return _client.post(f"/saves/{save_id}/pdf/apply", json=payload)
