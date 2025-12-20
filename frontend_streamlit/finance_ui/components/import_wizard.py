from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Any

import pandas as pd
import streamlit as st

from finance_ui.api import endpoints
from finance_ui.state import keys
from finance_ui.ui.messages import show_api_error
from finance_ui.utils.dates import from_api_date, safe_parse_date, to_api_date


@dataclass
class PreviewRow:
    # Minimal normalized row used by the UI
    id: str
    import_it: bool
    date: str
    name: str
    category: str
    type: str
    amount: float
    status: str | None = None


def _infer_confidence_flag(raw: dict[str, Any]) -> str:
    """
    Normalize to one of: 'high', 'low', 'failed'.

    Backend schema (current):
      item.status is a Dict[str, str] with values like TRUE/PARTIAL/FALSE/NONE.
    """
    s = raw.get("status")

    # Sometimes status is a simple string
    if isinstance(s, str):
        ls = s.lower()
        if "true" in ls or "high" in ls:
            return "high"
        if "false" in ls or "fail" in ls:
            return "failed"
        return "low"

    # Field-level dict statuses (preferred)
    st_map = raw.get("status_map") or raw.get("field_status") or raw.get("flags") or raw.get("status")
    if isinstance(st_map, dict):
        vals = [str(v).lower() for v in st_map.values()]
        if any("false" in v for v in vals):
            return "failed"
        if any(("none" in v) or ("partial" in v) for v in vals):
            return "low"
        return "high"

    return "low"


def _format_status_flags(st_map: Any) -> str:
    """
    Turns a field-status dict into a compact string for UI display.
    Example: "name:TRUE | amount:TRUE | date:PARTIAL"
    """
    if not isinstance(st_map, dict) or not st_map:
        return ""

    parts: list[str] = []
    for k, v in st_map.items():
        ks = str(k)
        vs = str(v)
        parts.append(f"{ks}:{vs}")

    s = " | ".join(parts)
    # keep table readable
    return s[:180]


def _normalize_preview_items(preview_payload: dict[str, Any]) -> list[PreviewRow]:
    """
    Tries to normalize backend payload into list[PreviewRow].
    Expected payload shape varies by backend; we support common patterns:
    - {"items": [...]} or {"candidates": [...]} or {"preview": [...]}
    Each item should contain transaction-like fields.
    """
    raw_items = None
    for k in ("items", "candidates", "preview", "transactions"):
        if k in preview_payload and isinstance(preview_payload[k], list):
            raw_items = preview_payload[k]
            break

    if raw_items is None:
        # Fallback if payload itself is a list
        if isinstance(preview_payload, list):
            raw_items = preview_payload
        else:
            raw_items = []

    out: list[PreviewRow] = []
    for idx, raw in enumerate(raw_items):
        if not isinstance(raw, dict):
            continue

        # Backend schema support:
        # PdfPreviewItem: { preview_id: str, candidate: {...tx fields...}, status: {field: status} }
        candidate = raw.get("candidate")
        if isinstance(candidate, dict):
            src = candidate
            rid = str(raw.get("preview_id") or raw.get("id") or idx)
        else:
            src = raw
            rid = str(raw.get("id") or raw.get("tx_id") or raw.get("preview_id") or idx)

        d = str(src.get("date") or "")
        name = str(src.get("name") or "")
        cat = str(src.get("category") or "unknown")
        t = str(src.get("type") or "")
        amt = src.get("amount", 0.0)
        try:
            amt_f = float(amt)
        except Exception:
            amt_f = 0.0

        conf = _infer_confidence_flag(raw)

        # Prefer showing backend field-status flags if present
        status_flags = raw.get("status") if isinstance(raw.get("status"), dict) else None
        status_str = _format_status_flags(status_flags) if status_flags else conf

        # Import defaults: high/low -> True, failed -> False
        import_default = True if conf in ("high", "low") else False

        out.append(
            PreviewRow(
                id=rid,
                import_it=import_default,
                date=d,
                name=name,
                category=cat,
                type=t,
                amount=amt_f,
                status=status_str,
            )
        )

    return out


def _rows_to_df(rows: list[PreviewRow]) -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "Import?": r.import_it,
                "date": r.date,
                "name": r.name,
                "amount": r.amount,
                "type": r.type,
                "category": r.category,
                "status": r.status or "",
                "_id": r.id,
            }
            for r in rows
        ]
    )


def _df_to_rows(df: pd.DataFrame) -> list[PreviewRow]:
    rows: list[PreviewRow] = []
    for _, r in df.iterrows():
        rows.append(
            PreviewRow(
                id=str(r.get("_id")),
                import_it=bool(r.get("Import?")),
                date=str(r.get("date") or ""),
                name=str(r.get("name") or ""),
                category=str(r.get("category") or "unknown"),
                type=str(r.get("type") or ""),
                amount=float(r.get("amount") or 0.0),
                status=str(r.get("status") or "") or None,
            )
        )
    return rows


def _validate_row(r: PreviewRow) -> tuple[bool, str | None]:
    # date must parse
    d = safe_parse_date(r.date)
    if d is None:
        return False, "Invalid date (must be DD.MM.YYYY)"
    # amount numeric already
    try:
        float(r.amount)
    except Exception:
        return False, "Invalid amount"
    # type must be valid
    if r.type not in ("I", "E"):
        return False, "Type must be I or E"
    return True, None


def render(save_id: str) -> None:
    ss = st.session_state
    step = int(ss.get(keys.IMPORT_STEP, 1))
    preview_payload = ss.get(keys.PDF_PREVIEW)

    st.markdown("## Import (PDF wizard)")

    # Step indicator
    st.caption(f"Step {step} / 4")

    if step == 1:
        _step1_upload()
    elif step == 2:
        _step2_preview(preview_payload)
    elif step == 3:
        _step3_fix_confirm(save_id, preview_payload)
    elif step == 4:
        _step4_result()
    else:
        ss[keys.IMPORT_STEP] = 1
        _step1_upload()


def _step1_upload() -> None:
    ss = st.session_state

    # Load parsers
    parsers: list[dict[str, Any]] = []
    try:
        with st.spinner("Loading parsers..."):
            out = endpoints.pdf_parsers()
        if isinstance(out, dict):
            parsers = out.get("items") or out.get("parsers") or []
        elif isinstance(out, list):
            parsers = out
    except Exception:
        # If endpoint isn't implemented, keep UI usable
        parsers = []

    parser_label_map: dict[str, str] = {}
    if parsers:
        for p in parsers:
            pid = str(p.get("id") or p.get("parser") or "")
            pname = str(p.get("name") or pid)
            if pid:
                parser_label_map[f"{pname} ({pid})"] = pid

    st.markdown("### Step 1 — Upload")
    file = st.file_uploader("PDF file", type=["pdf"])

    parser_choice: str | None = None
    if parser_label_map:
        label = st.selectbox("Parser", list(parser_label_map.keys()))
        parser_choice = parser_label_map[label]
    else:
        st.caption("Parser selector not available (no parsers endpoint or none returned).")

    year = st.text_input("Year (optional)", value="")

    if st.button("Preview", width="stretch", disabled=file is None):
        if file is None:
            return
        try:
            with st.spinner("Creating preview..."):
                payload = endpoints.pdf_preview(
                    file_bytes=file.getvalue(),
                    filename=file.name,
                    parser=parser_choice,
                    year=year.strip() or None,
                )
            ss[keys.PDF_PREVIEW] = payload
            ss[keys.IMPORT_STEP] = 2
            st.rerun()
        except Exception as e:
            show_api_error(e)


def _step2_preview(preview_payload: Any) -> None:
    ss = st.session_state

    st.markdown("### Step 2 — Preview")

    if not isinstance(preview_payload, (dict, list)):
        st.warning("No preview data. Go back and upload a PDF.")
        if st.button("Back to upload"):
            ss[keys.IMPORT_STEP] = 1
            st.rerun()
        return

    payload_dict = preview_payload if isinstance(preview_payload, dict) else {"items": preview_payload}
    rows = _normalize_preview_items(payload_dict)

    if not rows:
        st.warning("No transactions found in preview.")
    df = _rows_to_df(rows)

    c1, c2 = st.columns(2)
    if c1.button("Select all", width="stretch"):
        df["Import?"] = True
    if c2.button("Select none", width="stretch"):
        df["Import?"] = False

    # Editable table
    edited = st.data_editor(
        df.drop(columns=["_id"]),
        width="stretch",
        num_rows="fixed",
        disabled=["status"],
    )

    # Reattach ids
    edited["_id"] = df["_id"].values
    ss["pdf_preview_table"] = edited.to_dict(orient="records")

    if st.button("Continue", width="stretch"):
        ss[keys.IMPORT_STEP] = 3
        st.rerun()

    if st.button("Back", width="stretch"):
        ss[keys.IMPORT_STEP] = 1
        st.rerun()


def _step3_fix_confirm(save_id: str, preview_payload: Any) -> None:
    ss = st.session_state
    st.markdown("### Step 3 — Fix & confirm")

    records = ss.get("pdf_preview_table")
    if not isinstance(records, list) or not records:
        st.warning("No preview edits found. Go back to preview.")
        if st.button("Back to preview", width="stretch"):
            ss[keys.IMPORT_STEP] = 2
            st.rerun()
        return

    df = pd.DataFrame(records)

    # Keep only rows marked Import?
    df = df[df["Import?"] == True].copy()  # noqa: E712
    if df.empty:
        st.info("No rows selected for import.")
        if st.button("Back to preview", width="stretch"):
            ss[keys.IMPORT_STEP] = 2
            st.rerun()
        return

    st.caption("Edit values below. Date must be DD.MM.YYYY. Type must be I or E.")
    edited = st.data_editor(
        df.drop(columns=["_id"]),
        width="stretch",
        num_rows="fixed",
        disabled=["status"],
    )
    edited["_id"] = df["_id"].values

    # Validate rows
    rows = _df_to_rows(edited.assign(_id=edited["_id"]))
    problems: list[str] = []
    accepted: list[dict[str, Any]] = []

    for r in rows:
        ok, msg = _validate_row(r)
        if not ok:
            problems.append(f"{r.name or '(no name)'}: {msg}")
            continue

        # Convert date -> strict format (in case user entered a valid date-like string)
        d = safe_parse_date(r.date)
        assert d is not None

        accepted.append(
            {
                "date": to_api_date(d),
                "name": r.name,
                "amount": float(r.amount),
                "type": r.type,
                "category": r.category or "unknown",
            }
        )

    if problems:
        st.error("Some rows are invalid. Fix them before applying.")
        with st.expander("Details"):
            for p in problems:
                st.write(f"- {p}")
        return

    if st.button("Apply import", width="stretch"):
        try:
            with st.spinner("Applying import..."):
                endpoints.pdf_apply(save_id, accepted=accepted, source=None)
            ss[keys.LAST_ACTION_MSG] = f"Imported {len(accepted)} transactions ✓ You can Undo."
            ss[keys.TX_CACHE] = {}
            ss[keys.IMPORT_STEP] = 4
            st.rerun()
        except Exception as e:
            show_api_error(e)

    if st.button("Back to preview", width="stretch"):
        ss[keys.IMPORT_STEP] = 2
        st.rerun()


def _step4_result() -> None:
    ss = st.session_state
    st.markdown("### Step 4 — Result")

    msg = ss.get(keys.LAST_ACTION_MSG)
    if msg:
        st.success(msg)

    if st.button("Go to Transactions", width="stretch"):
        ss[keys.ACTIVE_PAGE] = "Transactions"
        ss[keys.IMPORT_STEP] = 1
        st.rerun()

    if st.button("Start another import", width="stretch"):
        ss[keys.PDF_PREVIEW] = None
        ss[keys.IMPORT_STEP] = 1
        st.rerun()
