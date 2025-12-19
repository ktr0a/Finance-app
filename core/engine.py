"""Core engine module (merged utils). Step 1 only."""

from __future__ import annotations

from .models import Result
from .ports import History, Repository

# Calculations with list of items & parameters (dicts). Returns
from config.calc_summary import (
    MONEY_FORMAT_MODE,
    INT_FORMAT_MODE,
    CURRENCY_SYMBOL,
    CALC_CONFIG,
)
from config.text import INVALID_TRANSACTION_TYPE


def format(value, mode: str) -> str:
    if mode == MONEY_FORMAT_MODE:
        return f"{value:.2f}{CURRENCY_SYMBOL}"
    if mode == INT_FORMAT_MODE:
        return str(value)
    return str(value)  # failsafe


def split_IE(transactions):  # seperate i/e
    income = []
    expense = []
    for i in range(len(transactions)):
        if transactions[i]["type"] == "I":
            income.append(transactions[i])
        elif transactions[i]["type"] == "E":
            expense.append(transactions[i])
        else:
            raise ValueError(
                INVALID_TRANSACTION_TYPE.format(
                    name=transactions[i]["name"],
                    type=transactions[i]["type"],
                )
            )
    return income, expense


def toti_raw(save) -> float:
    income, _ = split_IE(save)
    return sum(t["amount"] for t in income)


def tote_raw(save) -> float:
    _, expense = split_IE(save)
    return sum(t["amount"] for t in expense)


def netbal_raw(save) -> float:
    return toti_raw(save) - tote_raw(save)


def count_transactions(save) -> int:
    return len(save)


def avg_transaction_amount(save) -> float:
    if not save:
        return 0.0
    return sum(v["amount"] for v in save) / len(save)


def max_transaction_amount(save) -> float:
    if not save:
        return 0.0
    return max(v["amount"] for v in save)


def min_transaction_amount(save) -> float:
    if not save:
        return 0.0
    return min(v["amount"] for v in save)


CALC_FUNCTION_SEQUENCE = [
    toti_raw,
    tote_raw,
    netbal_raw,
    count_transactions,
    avg_transaction_amount,
    max_transaction_amount,
    min_transaction_amount,
]

CALC_FUNCTIONS = {
    label: func for (label, _), func in zip(CALC_CONFIG, CALC_FUNCTION_SEQUENCE)
}

# UTILS - imported by cli/cli.py
calc_util_func = [(label, CALC_FUNCTIONS[label], mode) for label, mode in CALC_CONFIG]


# Sorting utilities
from config.text import FILTER_BY_KEY_VALUE_LABEL


def filter_save(filterby_key, filterby_value, old_save) -> list:
    filtered_save = []

    for item in old_save:
        if filterby_key not in item:
            continue

        item_value = item[filterby_key]

        # Case-insensitive comparison for str
        if isinstance(item_value, str) and isinstance(filterby_value, str):
            if item_value.lower() == filterby_value.lower():
                filtered_save.append(item)

        # Exact comparison for other dtypes
        else:
            if item_value == filterby_value:
                filtered_save.append(item)

    return filtered_save


sort_util_func = [
    (FILTER_BY_KEY_VALUE_LABEL, filter_save),
]


# summarize with input from user
from datetime import datetime
from typing import Dict, Iterable, List, Sequence, Tuple, Union

from config.calc_summary import (
    REQUIRED_CALCS,
    SUMMARY_TEMPLATE,
    SUMMARY_KEY_MAP,
    CATEGORY_OVERVIEW_TITLE,
    INCOME_EXPENSE_OVERVIEW_TITLE,
    KEY_VALUE_PAIR_LABEL,
    TRANSACTIONS_ANALYZED_KEY,
    NET_BALANCE_LABEL,
)
from config.schema import DATE_FORMAT
from config.text import SUMMARY_OPTIONS, INCOME, EXPENSE


c_funcs = calc_util_func
s_funcs = sort_util_func


def initvars():
    return SUMMARY_TEMPLATE.copy()


def _safe_net_balance(dataset):
    """Compute net balance but ignore transactions with invalid 'type' values."""
    cleaned = [t for t in dataset if t.get("type") in ("I", "E")]
    if not cleaned:
        return 0.0
    return c_funcs[2][1](cleaned)


def _apply_calcs(summary, dataset):
    for label, func, _ in c_funcs:
        if label not in REQUIRED_CALCS:
            continue
        result = func(dataset)
        mapped_key = SUMMARY_KEY_MAP.get(label, label)
        summary[mapped_key] = result
    return summary


def summary_alltime(filterby_key, filterby_value, save):
    summary = initvars()
    summary[KEY_VALUE_PAIR_LABEL] = SUMMARY_OPTIONS[0]
    return _apply_calcs(summary, save)


def summary_general_overview(filterby_key, filterby_value, save):
    summary = {}
    summary["Special1"] = CATEGORY_OVERVIEW_TITLE
    summary[TRANSACTIONS_ANALYZED_KEY] = len(save)

    total_categories = list(set(item["category"] for item in save))
    summary["Total Categories"] = len(total_categories)

    category_list = []

    for category in total_categories:
        _, func = s_funcs[0]  # filter_save
        percategory_dict = {}

        filtered_save = func("category", category, save)
        percategory_dict["category_name"] = category
        percategory_dict["count"] = c_funcs[3][1](filtered_save)
        percategory_dict["total"] = c_funcs[2][1](filtered_save)
        category_list.append(percategory_dict)

    category_list.sort(key=lambda cat: cat["total"], reverse=True)

    summary["Categories"] = category_list
    summary[NET_BALANCE_LABEL] = _safe_net_balance(save)

    return summary


def summary_income_expense_overview(filterby_key, filterby_value, save):
    summary = {}
    summary["Special2"] = INCOME_EXPENSE_OVERVIEW_TITLE
    summary[TRANSACTIONS_ANALYZED_KEY] = len(save)

    total_types = ["I", "E"]

    for t in total_types:
        _, func = s_funcs[0]  # filter_save
        percategory_dict = {}

        filtered_save = func("type", t, save)
        percategory_dict["count"] = len(filtered_save)
        percategory_dict["total"] = _safe_net_balance(filtered_save)

        if t == "I":
            summary[INCOME] = percategory_dict
        else:
            summary[EXPENSE] = percategory_dict

    summary[NET_BALANCE_LABEL] = _safe_net_balance(save)

    return summary


def sum_by_key_value_pair(filterby_key, filterby_value, save):
    summary = initvars()
    _, func = s_funcs[0]  # filter_save
    filtered_save = func(filterby_key, filterby_value, save)
    summary[KEY_VALUE_PAIR_LABEL] = f"{filterby_key}: {filterby_value}"
    return _apply_calcs(summary, filtered_save)


def summary_by_daterange(filterby_key, filterby_value, save):
    summary = initvars()
    start_date_str, end_date_str = filterby_value
    start_date = datetime.strptime(start_date_str, DATE_FORMAT)
    end_date = datetime.strptime(end_date_str, DATE_FORMAT)

    filtered_save = []
    for transaction in save:
        transaction_date = datetime.strptime(transaction["date"], DATE_FORMAT)
        if start_date <= transaction_date <= end_date:
            filtered_save.append(transaction)

    summary[KEY_VALUE_PAIR_LABEL] = f"From {start_date_str} to {end_date_str}"
    return _apply_calcs(summary, filtered_save)


# Sum_utils - imported by cli/cli.py
sum_util_func = [  # DO NOT CHANGE ORDER - ORDER CRITICAL FOR SUMMARY OPTIONS
    (SUMMARY_OPTIONS[0], summary_alltime),
    (SUMMARY_OPTIONS[1], summary_general_overview),
    (SUMMARY_OPTIONS[2], summary_income_expense_overview),
    (SUMMARY_OPTIONS[3], sum_by_key_value_pair),
    (SUMMARY_OPTIONS[4], sum_by_key_value_pair),
    (SUMMARY_OPTIONS[5], sum_by_key_value_pair),
    (SUMMARY_OPTIONS[6], summary_by_daterange),
    (SUMMARY_OPTIONS[7], summary_by_daterange),
]


# ===== Engine Facade (Phase 1) =====


class Engine:
    def __init__(self, repo: Repository, history: History | None = None) -> None:
        self.repo = repo
        self.history = history

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

    def summary(self, *args, **kwargs) -> Result:
        try:
            summary_func = kwargs.pop("summary_func", None) or kwargs.pop("func", None)
            if summary_func is None:
                option = kwargs.pop("option", None)
                index = kwargs.pop("index", None)
                if option is not None:
                    for label, func in sum_util_func:
                        if label == option:
                            summary_func = func
                            break
                elif index is not None:
                    summary_func = sum_util_func[index][1]

            if summary_func is None:
                raise NotImplementedError("Phase 1: not wired yet")

            return Result(ok=True, data=summary_func(*args, **kwargs))
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
            return Result(ok=True, data=filter_save(filterby_key, filterby_value, transactions))
        except Exception as exc:
            return Result(ok=False, error=exc)

    def calc_menu(self) -> Result:
        menu = [(label, None, mode) for (label, _func, mode) in calc_util_func]
        return Result(ok=True, data=menu)

    def run_calc(self, choice: int, transactions) -> Result:
        try:
            label, func, mode = calc_util_func[choice - 1]
            result = func(transactions)
            output = format(result, mode)
            if "expense" in label.lower() and not output.startswith("-"):
                output = f"-{output}"
            return Result(ok=True, data=f"{label}: {output}")
        except Exception as exc:
            return Result(ok=False, error=exc)

    def format_value(self, value, mode: str) -> Result:
        try:
            return Result(ok=True, data=format(value, mode))
        except Exception as exc:
            return Result(ok=False, error=exc)

    def summary_menu(self) -> Result:
        menu = [(label, None) for (label, _func) in sum_util_func]
        return Result(ok=True, data=menu)

    def summary_template(self) -> Result:
        return Result(ok=True, data=SUMMARY_TEMPLATE)

    def create_backup(self, state) -> Result:
        try:
            if hasattr(self.repo, "_cr_backup_lst_like_core"):
                status = self.repo._cr_backup_lst_like_core(state)  # type: ignore[attr-defined]
                return Result(ok=True, data=status)

            from . import storage as st

            status = st.cr_backup_lst(state)
            return Result(ok=True, data=status)
        except Exception as exc:
            return Result(ok=False, error=exc)

    def list_backups(self) -> Result:
        try:
            if hasattr(self.repo, "_sort_backups_like_core"):
                backups = self.repo._sort_backups_like_core(ascending=False)  # type: ignore[attr-defined]
                return Result(ok=True, data=backups)

            from . import storage as st

            return Result(ok=True, data=st.list_backups())
        except Exception as exc:
            return Result(ok=False, error=exc)

    def restore_backup_file(self, path) -> Result:
        try:
            from pathlib import Path
            import json as _json

            file_path = Path(path)
            try:
                with file_path.open("r", encoding="utf-8") as f:
                    data = _json.load(f)
            except (OSError, _json.JSONDecodeError, TypeError, ValueError):
                return Result(ok=True, data=None)

            try:
                self.repo.save(data)
            except Exception:
                return Result(ok=True, data=False)

            return Result(ok=True, data=True)
        except Exception as exc:
            return Result(ok=False, error=exc)

    def restore_latest_backup(self) -> Result:
        try:
            backups_res = self.list_backups()
            if not backups_res.ok:
                return backups_res

            backups = backups_res.data or []
            if not backups:
                return Result(ok=True, data=None)

            newest = backups[0] # type: ignore
            restore_res = self.restore_backup_file(newest)
            if not restore_res.ok:
                return restore_res

            if restore_res.data is None:
                return Result(ok=True, data=None)
            if restore_res.data is False:
                return Result(ok=True, data=False)

            try:
                newest.unlink()
            except OSError:
                return Result(ok=True, data=False)

            return Result(ok=True, data=True)
        except Exception as exc:
            return Result(ok=False, error=exc)

    def delete_backup_files(self, backups) -> Result:
        try:
            cleanup_error = False
            for backup in backups:
                try:
                    if not backup.exists():
                        continue
                    backup.unlink()
                except OSError:
                    cleanup_error = True
            return Result(ok=True, data=cleanup_error)
        except Exception as exc:
            return Result(ok=False, error=exc)

    def push_undo_snapshot(self, state) -> Result:
        try:
            if hasattr(self.repo, "_cr_backup_lst_like_core"):
                status = self.repo._cr_backup_lst_like_core(  # type: ignore[attr-defined]
                    state, mode="undo", delbackup=False
                )
                return Result(ok=True, data=status)

            from . import storage as st

            status = st.cr_backup_lst(state, mode="undo", delbackup=False)
            return Result(ok=True, data=status)
        except Exception as exc:
            return Result(ok=False, error=exc)

    def clear_undo_stack(self) -> Result:
        try:
            if hasattr(self.repo, "undo_dir"):
                undo_dir = self.repo.undo_dir  # type: ignore[attr-defined]
                for f in undo_dir.glob("*.json"):
                    try:
                        f.unlink()
                    except OSError:
                        pass
                return Result(ok=True, data=True)

            from . import storage as st

            st.clear_undo_stack()
            return Result(ok=True, data=True)
        except Exception as exc:
            return Result(ok=False, error=exc)

    def clear_redo_stack(self) -> Result:
        try:
            if hasattr(self.repo, "redo_dir"):
                redo_dir = self.repo.redo_dir  # type: ignore[attr-defined]
                for f in redo_dir.glob("*.json"):
                    try:
                        f.unlink()
                    except OSError:
                        pass
                return Result(ok=True, data=True)

            from . import storage as st

            st.clear_redo_stack()
            return Result(ok=True, data=True)
        except Exception as exc:
            return Result(ok=False, error=exc)

    def session_backup(self, state) -> Result:
        try:
            if hasattr(self.repo, "_cr_backup_json_like_core"):
                self.repo._cr_backup_json_like_core()  # type: ignore[attr-defined]
            else:
                from . import storage as st

                st.cr_backup_json()

            return self.save_state(state)
        except Exception as exc:
            return Result(ok=False, error=exc)


class LegacyRepository:
    def load(self) -> object:
        from . import storage as st

        return st.load()

    def save(self, state: object) -> None:
        from . import storage as st

        status = st.save(state)
        if status is not True:
            raise RuntimeError("LegacyRepository.save failed")


class LegacyHistory:
    def undo(self) -> object:
        from . import storage as st

        return st.undo_action()

    def redo(self) -> object:
        from . import storage as st

        return st.redo_action()


def build_engine_legacy() -> Engine:
    repo = LegacyRepository()
    history = LegacyHistory()
    return Engine(repo=repo, history=history)


def build_engine_json() -> Engine:
    from config.storage import REDO_DIR_NAME, UNDO_DIR_NAME
    from infra.storage_json import JsonHistory, JsonRepository

    repo = JsonRepository(save_path="storage/save.json")
    history = JsonHistory(
        repo=repo,
        undo_dir=str(repo.storage_dir / UNDO_DIR_NAME),
        redo_dir=str(repo.storage_dir / REDO_DIR_NAME),
    )
    return Engine(repo=repo, history=history)
