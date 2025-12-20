from __future__ import annotations


def canon_category(raw: object) -> str:
    """
    Canonical category used for filtering/display:
    - strips whitespace
    - lowercases
    - maps empty/None/'none' -> 'unknown'
    """
    s = ""
    if raw is not None:
        try:
            s = str(raw).strip()
        except Exception:
            s = ""
    if not s or s.lower() == "none":
        return "unknown"
    return s.lower()
