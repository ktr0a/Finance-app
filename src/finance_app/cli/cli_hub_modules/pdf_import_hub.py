"""Hub utilities for importing transactions from PDF statements."""

from __future__ import annotations

from pathlib import Path

import finance_app.cli.helper as h
import finance_app.cli.prettyprint as pp
import finance_app.cli.ui.text as pr
from finance_app.core.schema import TRANSACTION_TYPES
from finance_app.config.storage import DEFAULT_DATE
from finance_app.infra.pdf.api import list_parsers, parse_pdf
from finance_app.infra.pdf.parameter import RAWDATA_DIR


def import_pdf_transactions(engine, *, purpose: str) -> list[dict] | None:
    pdf_path = _pick_pdf_path()
    if pdf_path is None:
        pp.highlight(pr.PDF_IMPORT_CANCELED)
        pp.pinput(pr.INPUT_ANY)
        return None

    parser_id = _pick_parser_id()
    if parser_id is None:
        pp.highlight(pr.PDF_IMPORT_CANCELED)
        pp.pinput(pr.INPUT_ANY)
        return None

    try:
        candidates = parse_pdf(pdf_path, parser_id=parser_id)
    except Exception:
        pp.highlight(pr.PDF_PARSE_FAILED)
        pp.pinput(pr.INPUT_ANY)
        return None

    if not candidates:
        pp.highlight(pr.PDF_NO_TRANSACTIONS)
        pp.pinput(pr.INPUT_ANY)
        return None

    reviewed = _review_candidates(candidates)
    if reviewed is None:
        pp.highlight(pr.PDF_IMPORT_CANCELED)
        pp.pinput(pr.INPUT_ANY)
        return None

    accepted_count = len(reviewed)
    skipped_count = len(candidates) - accepted_count

    print()
    print(pr.PDF_REVIEW_SUMMARY.format(accepted=accepted_count, skipped=skipped_count))
    print()

    if purpose == "new_save":
        confirm_prompt = pr.PDF_CONFIRM_NEW_SAVE
    else:
        confirm_prompt = pr.PDF_CONFIRM_ADD

    if not h.ask_yes_no(f"{confirm_prompt} {pr.YN}"):
        return None

    return reviewed


def _pick_pdf_path() -> str | None:
    pdf_dir = Path(RAWDATA_DIR)
    pdf_files = sorted(pdf_dir.glob("*.pdf")) if pdf_dir.exists() else []

    while True:
        pp.clearterminal()
        pp.highlight(pr.PDF_IMPORT_HUB)
        print()
        print(pr.PDF_SELECT_FILE)
        print()

        for idx, path in enumerate(pdf_files, start=1):
            print(f"{idx}. {path.name}")

        custom_idx = len(pdf_files) + 1
        print(f"{custom_idx}. {pr.PDF_CUSTOM_PATH}")
        print(f"0. {pr.EXIT}")
        print()

        choice_str = pp.pinput(pr.ENTER_ACC_NUMBER)
        choice = h.validate_numberinput(choice_str, custom_idx, allow_zero=True)
        if choice is None:
            continue

        if choice == 0:
            return None

        if choice == custom_idx:
            while True:
                custom_path = pp.pinput(f"{pr.PDF_CUSTOM_PATH}: ")
                if not custom_path:
                    pp.highlight(pr.PDF_FILE_NOT_FOUND)
                    continue
                if not Path(custom_path).exists():
                    pp.highlight(pr.PDF_FILE_NOT_FOUND)
                    continue
                return str(Path(custom_path))

        return str(pdf_files[choice - 1])


def _pick_parser_id() -> str | None:
    parsers = list_parsers()

    while True:
        pp.clearterminal()
        pp.highlight(pr.PDF_IMPORT_HUB)
        print()
        print(pr.PDF_SELECT_PARSER)
        print()

        for idx, (_, display_name) in enumerate(parsers, start=1):
            print(f"{idx}. {display_name}")
        print(f"0. {pr.EXIT}")
        print()

        choice_str = pp.pinput(pr.ENTER_ACC_NUMBER)
        choice = h.validate_numberinput(choice_str, len(parsers), allow_zero=True)
        if choice is None:
            continue

        if choice == 0:
            return None

        return parsers[choice - 1][0]


def _review_candidates(candidates: list[tuple[dict, dict]]) -> list[dict] | None:
    accepted: list[dict] = []
    total = len(candidates)

    for idx, (tx_raw, status_raw) in enumerate(candidates, start=1):
        tx = _ensure_tx_defaults(tx_raw)
        status = status_raw if isinstance(status_raw, dict) else {}

        while True:
            pp.clearterminal()
            pp.highlight(pr.PDF_IMPORT_HUB)
            print()
            print(pr.PDF_REVIEW_ITEM_LABEL.format(index=idx, total=total))
            print()

            _print_review_item(tx, status)
            print()
            print(pr.PDF_REVIEW_ACTIONS)
            print()

            actions = [
                pr.PDF_EDIT_FIELD.format(field="Name"),
                pr.PDF_EDIT_FIELD.format(field="Category"),
                pr.PDF_EDIT_FIELD.format(field="Type"),
                pr.PDF_EDIT_FIELD.format(field="Amount"),
                pr.PDF_EDIT_FIELD.format(field="Date"),
                pr.PDF_SKIP_ITEM,
                pr.PDF_ACCEPT_ITEM,
            ]
            for idx_action, label in enumerate(actions, start=1):
                print(f"{idx_action}. {label}")
            print(f"0. {pr.PDF_CANCEL_IMPORT}")
            print()

            choice_str = pp.pinput(pr.ENTER_ACC_NUMBER)
            choice = h.validate_numberinput(choice_str, len(actions), allow_zero=True)
            if choice is None:
                continue

            if choice == 0:
                return None

            if choice == 1:
                _edit_field(tx, "name")
                continue
            if choice == 2:
                _edit_field(tx, "category", allow_empty=True)
                continue
            if choice == 3:
                _edit_field(tx, "type")
                continue
            if choice == 4:
                _edit_field(tx, "amount")
                continue
            if choice == 5:
                _edit_field(tx, "date")
                continue
            if choice == 6:
                break
            if choice == 7:
                accepted.append(tx)
                break

        continue

    return accepted


def _ensure_tx_defaults(tx: dict) -> dict:
    tx_copy = dict(tx or {})
    tx_copy.setdefault("name", "unknown")
    tx_copy.setdefault("category", "unknown")
    tx_copy.setdefault("type", TRANSACTION_TYPES[0] if TRANSACTION_TYPES else "I")
    tx_copy.setdefault("amount", 0.0)
    tx_copy.setdefault("date", DEFAULT_DATE)
    return tx_copy


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


def _print_review_item(tx: dict, status: dict) -> None:
    keys = ["name", "category", "type", "amount", "date"]
    key_width = max(len(k) for k in keys)

    for key in keys:
        value = tx.get(key)
        status_label = _status_label(status.get(key))
        print(f"{key:<{key_width}} : {value} [{status_label}]")


def _edit_field(tx: dict, key: str, *, allow_empty: bool = False) -> None:
    while True:
        raw = pp.pinput(pr.PDF_EDIT_PROMPT)
        if allow_empty and raw.strip() == "":
            return
        value = h.validate_entry(key, raw)
        if value is None:
            continue
        tx[key] = value
        return



