from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
import inspect
import tempfile
import uuid

from finance_app.api.errors import InvalidRequestError, TransactionNotFoundError
from finance_app.api.services.save_registry import resolve_save_path
from finance_app.api.services.tx_id import ensure_ids
from finance_app.core.schema import DATE_FORMAT
from finance_app.config.storage import BACKUP_DIR_NAME, BACKUP_FILE_PREFIX, REDO_DIR_NAME, UNDO_DIR_NAME
from finance_app.core.engine import Engine
from finance_app.infra.storage_json import JsonHistory, JsonRepository
from finance_app.infra.pdf.api import list_parsers, parse_pdf
from finance_app.core.schema import TRANSACTION_TYPES
from finance_app.config.storage import DEFAULT_DATE


@dataclass
class TransactionsResult:
    items: list[dict]
    total: int
    limit: int
    offset: int


def _parse_date(value: str) -> datetime:
    return datetime.strptime(value, DATE_FORMAT)


def _safe_parse_date(value: str | None) -> datetime:
    if not isinstance(value, str):
        return datetime.min
    try:
        return _parse_date(value)
    except ValueError:
        return datetime.min


def _build_engine(save_id: str) -> Engine:
    save_path = resolve_save_path(save_id)
    repo = JsonRepository(save_path=str(save_path))
    history = JsonHistory(
        repo=repo,
        undo_dir=str(repo.storage_dir / UNDO_DIR_NAME),
        redo_dir=str(repo.storage_dir / REDO_DIR_NAME),
    )
    return Engine(repo=repo, history=history)


def _load_transactions(save_id: str) -> tuple[Engine, list[dict]]:
    engine = _build_engine(save_id)
    res = engine.list_transactions()
    if not res.ok:
        raise InvalidRequestError("Failed to load transactions")

    transactions = res.data or []
    if not isinstance(transactions, list):
        raise InvalidRequestError("Save data is not a transaction list")

    transactions, changed = ensure_ids(transactions)
    if changed:
        save_res = engine.save_state(transactions)
        if not save_res.ok:
            raise InvalidRequestError("Failed to persist transaction ids")

    return engine, transactions


def _find_tx_index(transactions: list[dict], tx_id: str) -> int:
    for idx, tx in enumerate(transactions):
        if tx.get("id") == tx_id:
            return idx
    raise TransactionNotFoundError(f"Transaction '{tx_id}' not found")


def _status_label(value) -> str:
    if value is None:
        return "NONE"
    name = getattr(value, "name", None)
    if name:
        return str(name)
    if isinstance(value, bool):
        return "TRUE" if value else "FALSE"
    if isinstance(value, int):
        lookup = {0: "NONE", 1: "FALSE", 2: "PARTIAL", 3: "TRUE"}
        return lookup.get(value, str(value))
    return str(value)


def _ensure_tx_defaults(tx: dict) -> dict:
    tx_copy = dict(tx or {})
    tx_copy.setdefault("name", "unknown")
    tx_copy.setdefault("category", "unknown")
    tx_copy.setdefault("type", TRANSACTION_TYPES[0] if TRANSACTION_TYPES else "I")
    tx_copy.setdefault("amount", 0.0)
    tx_copy.setdefault("date", DEFAULT_DATE)
    return tx_copy


def _ensure_parseable_date(value: str | None) -> datetime | None:
    if value is None:
        return None
    if not value.strip():
        raise InvalidRequestError("date must be a non-empty string")
    try:
        return _parse_date(value)
    except ValueError as exc:
        raise InvalidRequestError("Invalid date format") from exc


def _parse_backup_created_at(name: str) -> str | None:
    stem = Path(name).stem
    if not stem.startswith(BACKUP_FILE_PREFIX):
        return None
    suffix = stem[len(BACKUP_FILE_PREFIX):]
    for fmt in ("%Y%m%d_%H%M%S_%f", "%Y%m%d_%H%M%S"):
        try:
            return datetime.strptime(suffix, fmt).isoformat()
        except ValueError:
            continue
    return None


def _backup_restore_result(res: bool | None, *, success_message: str) -> dict:
    if res is True:
        return {"ok": True, "message": success_message}
    if res is False:
        return {"ok": False, "message": "Backup restore failed."}
    return {"ok": False, "message": "No backups found."}


def _validate_transactions_query(
    *,
    type: str | None,
    sort: str | None,
    order: str | None,
    limit: int,
    offset: int,
    date_from: str | None,
    date_to: str | None,
) -> tuple[datetime | None, datetime | None]:
    if limit < 0 or offset < 0:
        raise InvalidRequestError("limit/offset must be non-negative")

    if type is not None and type not in ("I", "E"):
        raise InvalidRequestError("type must be 'I' or 'E'")

    allowed_sort = {"date", "amount", "name", "category", "type", "id"}
    if sort is not None and sort not in allowed_sort:
        raise InvalidRequestError(f"sort must be one of {sorted(allowed_sort)}")

    if order is not None and order not in ("asc", "desc"):
        raise InvalidRequestError("order must be 'asc' or 'desc'")

    from_dt = _ensure_parseable_date(date_from) if date_from is not None else None
    to_dt = _ensure_parseable_date(date_to) if date_to is not None else None

    if from_dt and to_dt and from_dt > to_dt:
        raise InvalidRequestError("date_from must be before or equal to date_to")

    return from_dt, to_dt


class FinanceService:
    """Thin adapter around core/infra for API use."""

    def list_transactions(
        self,
        save_id: str,
        *,
        q: str | None = None,
        type: str | None = None,
        category: str | None = None,
        date_from: str | None = None,
        date_to: str | None = None,
        sort: str | None = None,
        order: str | None = None,
        limit: int = 200,
        offset: int = 0,
    ) -> TransactionsResult:
        """Return filtered/sorted transactions with paging metadata."""
        _, transactions = _load_transactions(save_id)

        items = transactions

        from_dt, to_dt = _validate_transactions_query(
            type=type,
            sort=sort,
            order=order,
            limit=limit,
            offset=offset,
            date_from=date_from,
            date_to=date_to,
        )

        if q:
            needle = q.lower()
            items = [t for t in items if needle in str(t.get("name", "")).lower()]

        if type:
            items = [t for t in items if t.get("type") == type]

        if category:
            cat_lower = category.lower()
            items = [t for t in items if str(t.get("category", "")).lower() == cat_lower]

        if from_dt or to_dt:
            filtered: list[dict] = []
            for t in items:
                raw_date = t.get("date")
                if not isinstance(raw_date, str):
                    continue
                try:
                    tx_date = _parse_date(raw_date)
                except ValueError:
                    continue

                if from_dt and tx_date < from_dt:
                    continue
                if to_dt and tx_date > to_dt:
                    continue
                filtered.append(t)
            items = filtered

        if sort is None:
            items = sorted(items, key=lambda t: str(t.get("name", "")).lower())
            items = sorted(items, key=lambda t: _safe_parse_date(t.get("date")), reverse=True)
        else:
            sort_key = None
            if sort in ("date", "amount", "name", "category", "type", "id"):
                if sort == "date":
                    sort_key = lambda t: _safe_parse_date(t.get("date"))
                elif sort == "amount":
                    sort_key = lambda t: float(t.get("amount", 0.0))
                else:
                    sort_key = lambda t: str(t.get(sort, "")).lower()

            if sort_key is not None:
                if order is None:
                    order = "desc" if sort == "date" else "asc"
                reverse = order == "desc"
                items = sorted(items, key=sort_key, reverse=reverse)

        total = len(items)
        if limit == 0:
            page_items = items[offset:]
        else:
            page_items = items[offset : offset + limit]

        return TransactionsResult(items=page_items, total=total, limit=limit, offset=offset)

    def create_transaction(self, save_id: str, tx: dict) -> dict:
        """Create a new transaction in the save."""
        engine, _ = _load_transactions(save_id)

        tx_copy = dict(tx)
        tx_copy["id"] = str(uuid.uuid4())

        res = engine.add_transaction(tx_copy)
        if not res.ok:
            raise InvalidRequestError("Failed to add transaction")

        return tx_copy

    def update_transaction(self, save_id: str, tx_id: str, patch: dict) -> dict:
        """Update fields for a transaction by id."""
        engine, transactions = _load_transactions(save_id)
        idx = _find_tx_index(transactions, tx_id)

        current = dict(transactions[idx])
        for key, value in patch.items():
            if value is not None:
                current[key] = value
        current["id"] = tx_id

        res = engine.edit_transaction(idx, new_tx=current)
        if not res.ok:
            raise InvalidRequestError("Failed to update transaction")

        return current

    def delete_transaction(self, save_id: str, tx_id: str) -> bool:
        """Delete a transaction by id."""
        engine, transactions = _load_transactions(save_id)
        idx = _find_tx_index(transactions, tx_id)

        res = engine.delete_transaction(idx)
        if not res.ok:
            raise InvalidRequestError("Failed to delete transaction")

        return True

    def get_transaction(self, save_id: str, tx_id: str) -> dict:
        """Return a single transaction by id."""
        _, transactions = _load_transactions(save_id)
        idx = _find_tx_index(transactions, tx_id)
        return dict(transactions[idx])

    def summary(self, save_id: str) -> dict:
        """Compute summary totals for a save."""
        _, transactions = _load_transactions(save_id)

        income_total = 0.0
        expense_total = 0.0
        by_category: dict[str, float] = {}
        by_month: dict[str, dict[str, float]] = {}
        warnings: list[str] = []

        for idx, tx in enumerate(transactions, start=1):
            raw_amount = tx.get("amount", 0.0)
            try:
                amount = float(raw_amount)
            except (TypeError, ValueError):
                warnings.append(f"Transaction {idx}: invalid amount")
                continue

            tx_type = tx.get("type")
            category = str(tx.get("category", "unknown"))

            if tx_type == "I":
                income_total += amount
                signed = amount
            elif tx_type == "E":
                expense_total += amount
                signed = -amount
            else:
                warnings.append(f"Transaction {idx}: invalid type")
                signed = 0.0

            by_category[category] = by_category.get(category, 0.0) + signed

            raw_date = tx.get("date")
            if isinstance(raw_date, str):
                try:
                    tx_date = _parse_date(raw_date)
                    month_key = tx_date.strftime("%Y-%m")
                except ValueError:
                    warnings.append(f"Transaction {idx}: invalid date")
                    month_key = None
            else:
                warnings.append(f"Transaction {idx}: invalid date")
                month_key = None

            if month_key:
                month_entry = by_month.setdefault(
                    month_key,
                    {"I": 0.0, "E": 0.0, "net": 0.0},
                )
                if tx_type == "I":
                    month_entry["I"] += amount
                elif tx_type == "E":
                    month_entry["E"] += amount
                month_entry["net"] = month_entry["I"] - month_entry["E"]

        net_total = income_total - expense_total

        return {
            "income_total": income_total,
            "expense_total": expense_total,
            "net_total": net_total,
            "currency": None,
            "by_category": by_category or None,
            "by_type": {"I": income_total, "E": expense_total},
            "by_month": by_month or None,
            "warnings": warnings,
        }

    def undo(self, save_id: str) -> bool:
        """Undo the most recent mutation if available."""
        engine = _build_engine(save_id)
        res = engine.undo()
        if not res.ok:
            raise InvalidRequestError("Failed to undo")

        if not isinstance(res.data, tuple) or len(res.data) != 2:
            raise InvalidRequestError("Undo not available")

        status, _save = res.data
        if status is not True:
            raise InvalidRequestError("Undo not available")

        _load_transactions(save_id)
        return True

    def redo(self, save_id: str) -> bool:
        """Redo the most recently undone mutation if available."""
        engine = _build_engine(save_id)
        res = engine.redo()
        if not res.ok:
            raise InvalidRequestError("Failed to redo")

        if not isinstance(res.data, tuple) or len(res.data) != 2:
            raise InvalidRequestError("Redo not available")

        status, _save = res.data
        if status is not True:
            raise InvalidRequestError("Redo not available")

        _load_transactions(save_id)
        return True

    def history(self, save_id: str) -> dict:
        """Return undo/redo availability and depth information."""
        save_path = resolve_save_path(save_id)
        repo = JsonRepository(save_path=str(save_path))

        undo_dir = Path(repo.storage_dir) / UNDO_DIR_NAME
        redo_dir = Path(repo.storage_dir) / REDO_DIR_NAME

        undo_count = len(list(undo_dir.glob(f"{BACKUP_FILE_PREFIX}*.json"))) if undo_dir.exists() else 0
        redo_count = len(list(redo_dir.glob(f"{BACKUP_FILE_PREFIX}*.json"))) if redo_dir.exists() else 0

        return {
            "undo_available": undo_count > 0,
            "redo_available": redo_count > 0,
            "undo_depth": undo_count,
            "redo_depth": redo_count,
        }

    def list_backups(self, save_id: str) -> list[dict]:
        save_path = resolve_save_path(save_id)
        repo = JsonRepository(save_path=str(save_path))
        hist = JsonHistory(repo)
        _ = Engine(repo, hist)

        backups = repo.list_backups()
        out: list[dict] = []
        for p in backups:
            out.append(
                {
                    "filename": p.name,
                    "path": str(p),
                    "created_at": _parse_backup_created_at(p.name),
                }
            )
        return out

    def restore_latest_backup(self, save_id: str) -> dict:
        save_path = resolve_save_path(save_id)
        repo = JsonRepository(save_path=str(save_path))
        hist = JsonHistory(repo)
        engine = Engine(repo, hist)

        res = engine.restore_latest_backup()
        return _backup_restore_result(res, success_message="Backup restored (latest).")

    def restore_backup_file(self, save_id: str, path: str) -> dict:
        save_path = resolve_save_path(save_id)
        repo = JsonRepository(save_path=str(save_path))
        hist = JsonHistory(repo)
        engine = Engine(repo, hist)

        backup_dir = save_path.parent / BACKUP_DIR_NAME
        try:
            target = Path(path).resolve()
            backup_root = backup_dir.resolve()
        except Exception:
            return {"ok": False, "message": "Invalid backup path."}

        if backup_root not in target.parents:
            return {"ok": False, "message": "Invalid backup path."}

        res = engine.restore_backup_file(Path(path))
        return _backup_restore_result(res, success_message="Backup restored.")

    def pdf_preview(self, file_bytes: bytes, *, parser: str = "auto", year: str | None = None) -> dict:
        """Parse a PDF into preview candidates without persisting."""
        if not file_bytes:
            raise InvalidRequestError("PDF file is empty")

        response_warnings: list[str] = []

        parser_info = self.list_pdf_parsers()
        parser_map = {item["id"]: item["name"] for item in parser_info["items"]}

        parser_requested = parser
        parser_used = parser_requested
        if parser_requested == "auto" and parser_map:
            if "erste" in parser_map:
                parser_used = "erste"
            else:
                parser_used = sorted(parser_map.keys())[0]
        elif parser_requested == "auto" and not parser_map:
            response_warnings.append("parser auto requested but available parsers are unknown")

        if parser_requested != "auto" and parser_map and parser_requested not in parser_map:
            raise InvalidRequestError(f"parser must be one of {sorted(parser_map.keys())}")

        with tempfile.TemporaryDirectory() as temp_dir:
            tmp_path = Path(temp_dir) / "upload.pdf"
            tmp_path.write_bytes(file_bytes)

            try:
                parse_kwargs: dict[str, str] = {}
                if year is not None:
                    signature = inspect.signature(parse_pdf)
                    if "year" in signature.parameters:
                        parse_kwargs["year"] = year
                    elif "yr" in signature.parameters:
                        parse_kwargs["yr"] = year
                    elif any(
                        param.kind == param.VAR_KEYWORD
                        for param in signature.parameters.values()
                    ):
                        parse_kwargs["year"] = year
                    else:
                        response_warnings.append(
                            "year parameter provided but parser does not support it"
                        )

                candidates = parse_pdf(
                    str(tmp_path),
                    parser_id=parser_used,
                    **parse_kwargs,
                )
            except Exception as exc:
                raise InvalidRequestError("PDF parse failed") from exc

        items: list[dict] = []
        for tx_raw, status_raw in candidates:
            tx = _ensure_tx_defaults(tx_raw)
            status_dict = status_raw if isinstance(status_raw, dict) else {}
            status = {key: _status_label(value) for key, value in status_dict.items()}
            warnings: list[str] = []

            for key in ("name", "amount", "date", "type", "category"):
                if key not in status:
                    status[key] = "NONE"

            for key, label in status.items():
                if label not in ("TRUE", "PARTIAL"):
                    warnings.append(f"{key}: {label}")

            items.append({
                "preview_id": uuid.uuid4().hex,
                "candidate": tx,
                "status": status,
                "warnings": warnings,
            })

        return {
            "items": items,
            "parser": parser_used or parser_requested,
            "parser_requested": parser_requested,
            "parser_used": parser_used,
            "warnings": response_warnings,
            "parser_display": parser_map.get(parser_used),
        }

    def list_pdf_parsers(self) -> dict:
        """List registered PDF parsers."""
        try:
            raw = list_parsers()
        except Exception:
            return {"items": []}

        items: list[dict] = []
        if isinstance(raw, dict):
            for parser_id, name in raw.items():
                items.append({"id": str(parser_id), "name": str(name)})
        elif isinstance(raw, list):
            for entry in raw:
                if isinstance(entry, dict):
                    pid = entry.get("id")
                    name = entry.get("name")
                    if pid and name:
                        items.append({"id": str(pid), "name": str(name)})
                elif isinstance(entry, (tuple, list)) and len(entry) >= 2:
                    items.append({"id": str(entry[0]), "name": str(entry[1])})
        items.sort(key=lambda item: item["id"])
        return {"items": items}

    def pdf_apply(self, save_id: str, accepted: list[dict], *, source: str | None = None) -> dict:
        """Persist accepted PDF transactions into a save."""
        _ = source
        if not accepted:
            return {"added": 0, "skipped": 0, "warnings": []}

        engine, _ = _load_transactions(save_id)

        to_add: list[dict] = []
        warnings: list[str] = []
        skipped = 0
        for idx, tx in enumerate(accepted, start=1):
            tx_copy = dict(tx)
            tx_type = tx_copy.get("type")
            if tx_type not in ("I", "E"):
                warnings.append(f"Item {idx}: invalid type")
                skipped += 1
                continue

            raw_amount = tx_copy.get("amount")
            try:
                tx_copy["amount"] = float(raw_amount)
            except (TypeError, ValueError):
                warnings.append(f"Item {idx}: invalid amount")
                skipped += 1
                continue

            raw_date = tx_copy.get("date")
            if not isinstance(raw_date, str) or not raw_date.strip():
                warnings.append(f"Item {idx}: invalid date")
                skipped += 1
                continue

            tx_copy["id"] = str(uuid.uuid4())
            to_add.append(tx_copy)

        if to_add:
            res = engine.import_transactions(to_add)
            if not res.ok:
                raise InvalidRequestError("Failed to import transactions")

        return {
            "added": len(to_add),
            "skipped": skipped,
            "warnings": warnings,
        }
