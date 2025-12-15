import re
from typing import Any

import pdf_handeling.parameter as p
import cli.helper as h
from config.storage import DEFAULT_DATE
from config.schema import TRANSACTION_TYPES

from enum import IntEnum

class Status(IntEnum):
    NONE = 0
    FALSE = 1
    PARTIAL = 2
    TRUE = 3


def _initdefiners():
    from core.core_config import initvars

    _, definers, _, _ = initvars()
    return definers


"""Pseudocode:

- [0] & [3] = possible Names
- [1] Standard date 
- [2] of item = eur amount

"""
# last item of 1st line
def amount_type_per_item(word: list, markers: tuple[float, float, float, float]) -> tuple[Status, str | float, str | None]:
    
    x0, y0, x1, y1, text, block_no, line_no, word_no = word
    validx0, validy0, validx1, validy1 = markers

    text = text.strip()

    text = _normalize_money_token(text)
    
    # if not _is_between(x1, validx1, p.VARIANCE + p.EXTRA_MARGIN):
    #    return (Status.NONE, "0", None)
    
    definers = _initdefiners()
    akey = definers[3][0]

    value = h.validate_entry(akey, text)

    if value is None: # is amount valid
        return (Status.FALSE, "1", None)
    
    elif "-" in text:
        ttype = TRANSACTION_TYPES[1]
    else: ttype = TRANSACTION_TYPES[0]

    
    return (Status.TRUE, value, ttype)

# 2nd to last item of 1st line
def date_per_item(dateword: list, amountword: list, yr: str | None = None) -> tuple[Status, str]:

    x0, y0, x1, y1, text, block_no, line_no, word_no = dateword
    validx0, validy0, validx1, validy1, *_ = amountword

    text = text.strip()
    if p.DEBUG_FLAG is True: print(text)

    # Item doesnt quality
    if not _is_between(y0, validy0, p.VARIANCE) and _is_between(y1, validy1, p.VARIANCE):
        return (Status.NONE, "0")

    # Numeric
    if not text.isdigit():
        return (Status.FALSE, "1")

    # DDMM format
    if len(text) == 4:
        dd = text[:2]
        mm = text[2:]

        # Determine usable year
        if yr and yr.isdigit() and len(yr) == 4:
            yyyy = yr
            using_detected_year = True
        else:
            yyyy = DEFAULT_DATE[-4:]
            using_detected_year = False

        raw = f"{dd}.{mm}.{yyyy}"

        definers = _initdefiners()
        key = definers[4][0]

        value = h.validate_entry(key, raw)

        if value is None:
            return (Status.FALSE, "1.1")

        # Choose status based on where yyyy comes from
        if using_detected_year:
            return (Status.TRUE, value) #type: ignore
        else:
            return (Status.PARTIAL, value) #type: ignore

    return (Status.FALSE, f"invalid_length:{len(text)}")

def _name_item_formatter(transaction: list) -> list:
    wordlst = []
    perline = []
    prevline = None
    for word in transaction:
        if prevline == None:
            prevline = word[6]

        if prevline == word[6]:
            perline.append(word[4])
        else:
            wordlst.append(perline)
            prevline = word[6]
            perline = []
            perline.append(word[4])
    if perline:
        wordlst.append(perline)

    return wordlst

def _name_filter(transaction: list[list[str]]) -> list | None:
    cleaned: list[list[str]] = []
    seen_lines: set[tuple[str, ...]] = set()

    for line in transaction:
        newline: list[str] = []

        for word in line:
            w = word.strip().lower()

            # Blacklist 
            if any(w.startswith(prefix.lower().strip()) for prefix in p.NAME_MAPPING_BLACKLIST):
                continue

            newline.append(w)

        if newline: # Dedupe (perline and overall)
            newline = _name_dedupe_words_in_line(newline) 
            line_key = tuple(newline)

            if line_key not in seen_lines:
                seen_lines.add(line_key)
                cleaned.append(newline)

    cleaned = _name_remove_subset_lines(cleaned)
    cleaned = _name_drop_date_lines(cleaned)

    if cleaned is None:
        return None

    return cleaned

def _name_dedupe_words_in_line(line: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for w in line:
        if w not in seen:
            seen.add(w)
            result.append(w)
    return result

def _name_remove_subset_lines(lines: list[list[str]]) -> list[list[str]]: # disabled for now
    return lines
    result: list[list[str]] = []
    sets = [set(line) for line in lines]

    for i, line in enumerate(lines):
        s = sets[i]
        # check if s is a proper subset of any other set
        if any(s < other for j, other in enumerate(sets) if i != j):
            continue
        result.append(line)

    return result

def _name_flatten_lst(wordlst_perline: list[list[str]]) -> list[str]:
    wordlst = []
    for line in wordlst_perline:
        wordlst.extend(line)

    return wordlst

def _name_drop_date_lines(lines: list[list[str]]) -> list[list[str]]: # Failsafe
    out = []
    for line in lines:
        if len(line) == 1 and line[0].isdigit() and len(line[0]) == 4:
            continue
        out.append(line)
    return out


def _normalize_token(tok: str) -> str:
    """
    Normalize token for comparisons:
    - lowercase
    - strip common surrounding punctuation
    Keep internal punctuation (e.g. 's.a') because it's meaningful for legal detection.
    """
    return tok.lower().strip(" \t\n\r.,;:!?'\"()[]{}<>")

def _token_has_digits(tok: str) -> bool:
    return any(ch.isdigit() for ch in tok)

def _token_is_long_digit_id(tok: str) -> bool:
    """
    Detect very long digit-heavy tokens like '1045047095378'
    """
    t = tok.strip()
    if len(t) < 8:
        return False
    digit_count = sum(ch.isdigit() for ch in t)
    return digit_count >= 8 and digit_count / max(1, len(t)) >= 0.8

def _punct_cost(text: str) -> float:
    """
    Sum punctuation weights based on p.PUNCT_CHARS. Uses count() so repeated chars cost more.
    """
    cost = 0.0
    for ch, w in p.PUNCT_CHARS:
        if ch in text:
            cost += w * text.count(ch)
    return cost

def _looks_url_like(text_lower: str) -> bool:
    """
    URL / email heuristic. Very strong 'not a merchant name' indicator.
    """
    return any(x in text_lower for x in ("http", "www", ".com", ".net", ".org", "@"))


def _name_scoring_calc_plus(text: str) -> float:
    """
    Add points for 'name-like' properties.
    """
    text = text.strip()
    if not text:
        return 0.0

    weights = p.NAME_SCORING_WEIGHTS

    # Tokenize by whitespace (safe because we build candidate strings with spaces)
    tokens = [t for t in text.split() if t]

    # Reward letters (merchant names have letters)
    letters = sum(ch.isalpha() for ch in text)
    plus = letters * weights["letters_bonus_per_char"]

    # Reward word-count sweet spot (typical merchant names are 2–6 words)
    wc = len(tokens)
    if 2 <= wc <= 6:
        plus += weights["sweetspot_wordcount_bonus"]

    # Reward average token length (filters out initials/legal fragments dominating)
    avg_len = sum(len(t) for t in tokens) / max(1, wc)
    if avg_len >= 4:
        plus += weights["avg_token_len_bonus"]

    # Reward strong, brand-like tokens (alphabetic, length >= 4)
    # This helps lines like "paypal (europe) s.a ..." still win despite legal noise.
    for tok in tokens:
        norm = _normalize_token(tok)
        if len(norm) >= 4 and norm.isalpha():
            plus += 2.0


    return float(plus)

def _name_scoring_calc_minus(text: str) -> float:
    """
    Subtract points for metadata/noise properties.
    Uses token-based checks so spaces do not break detection.
    """
    text_raw = text.strip()
    if not text_raw:
        return 0.0

    weights = p.NAME_SCORING_WEIGHTS
    text_lower = text_raw.lower()

    minus = 0.0

    # Heavy penalty for URL/email patterns
    if _looks_url_like(text_lower):
        minus += weights["url_like_penalty"]

    # Weighted punctuation cost
    minus += weights["punct_weight_multiplier"] * _punct_cost(text_raw)

    # Token-level penalties
    tokens = [t for t in text_raw.split() if t]
    for tok in tokens:
        norm = _normalize_token(tok)

        # penalize long digit-heavy IDs
        if _token_is_long_digit_id(tok):
            minus += weights["long_digit_id_penalty"]
            # if this is present, it's usually very noisy. Still continue to score other tokens.

        # penalize any digit presence (milder than long ID)
        elif _token_has_digits(tok):
            minus += weights["digit_token_penalty"]

        # penalize legal/company-form tokens
        # normalize internal dots a bit (so "s.a." becomes "s.a")
        norm_legal = norm.rstrip(".")
        is_legal = norm_legal in p.LEGAL_TOKENS

        # penalize short tokens (e.g. "x", "a.") ONLY if they are NOT legal tokens
        # because legal tokens already get their own penalty.
        if len(norm) <= 2 and norm and not is_legal:
            minus += weights["short_token_penalty"]

        # penalize legal/company-form tokens (mildly)
        if is_legal:
            minus += weights["legal_token_penalty"]

    return float(minus)

def _name_scoring_find_highestscore(lst: list[tuple[str, float, float, float]]) -> str | None:
    MIN_SCORE = -9999.0

    if not lst:
        return None

    # sort by:
    # 1) score
    # 2) length of text
    lst.sort(
        key=lambda x: (x[3], len(x[0])),
        reverse=True
    )

    best = lst[0]
    if best[3] < MIN_SCORE:
        return None

    return best[0]


def _name_scoring_cleanline(linestr: str) -> str:
    """
    Convert the chosen candidate string into a clean merchant name:
    - remove legal tokens (gmbh, s.a, r.l, etc.)
    - remove tiny tokens and punctuation-only tokens
    - keep up to p.NAME_OUTPUT_MAX_TOKENS informative tokens
    """
    tokens = [t for t in linestr.split() if t]
    cleaned: list[str] = []

    for tok in tokens:
        norm = _normalize_token(tok)

        # skip empty / punctuation-only
        if not norm:
            continue

        # skip very short fragments
        if len(norm) <= 2:
            continue

        # skip legal tokens
        norm_legal = norm.rstrip(".")
        if norm_legal in p.LEGAL_TOKENS:
            continue

        # unwrap parentheses for words like "(europe)" -> "europe"
        norm_unwrap = norm.strip("()[]{}")
        if not norm_unwrap:
            continue

        cleaned.append(norm_unwrap)

    if not cleaned:
        return ""

    # Decide how many tokens to output
    max_tokens = getattr(p, "NAME_OUTPUT_MAX_TOKENS", 2)
    cleaned = cleaned[:max_tokens]

    return " ".join(cleaned).strip()


def name_scoring_main(cleaned: list[list[str]]) -> str | None:
    scored: list[tuple[str, float, float, float]] = []

    # Optional safety net: drop single-token 4-digit lines like "2509" (DDMM date)
    if getattr(p, "NAME_DROP_DATE_LIKE_LINES", True):
        cleaned = [
            line for line in cleaned
            if not (len(line) == 1 and line[0].isdigit() and len(line[0]) == 4)
        ]

    for line in cleaned:
        linestr = " ".join(line).strip()
        if not linestr:
            continue

        plus = _name_scoring_calc_plus(linestr)
        minus = _name_scoring_calc_minus(linestr)
        scored.append((linestr, plus, minus, plus - minus))

    if p.DEBUG_FLAG is True:
        print("DEBUG: SCORED CANDIDATES")
        for t, plus, minus, score in scored:
            print(f"  '{t}' -> plus={plus:.2f}, minus={minus:.2f}, score={score:.2f}")


    highestline = _name_scoring_find_highestscore(scored)

    if highestline is not None:
        final = _name_scoring_cleanline(highestline)
        return final if final else highestline  # fallback to raw if cleaning empties it

    return None


def _word_key(word: list[Any]) -> tuple[int, int, int]:
    """
    Stable identifier for a word row from PyMuPDF 'words' output.
    """
    block_no = int(word[5])
    line_no = int(word[6])
    word_no = int(word[7])
    return (block_no, line_no, word_no)


def _remove_words(transaction_words: list[list[Any]], remove_words: list[list[Any] | None]) -> list[list[Any]]:
    """
    Return a new list where the chosen words (amount/date) are removed.
    Removal uses (block_no, line_no, word_no) keys for safety.
    """
    remove_keys: set[tuple[int, int, int]] = set()
    for w in remove_words:
        if w is None:
            continue
        remove_keys.add(_word_key(w))

    if not remove_keys:
        return transaction_words[:]  # no changes

    out: list[list[Any]] = []
    for w in transaction_words:
        if _word_key(w) in remove_keys:
            continue
        out.append(w)
    return out


def _is_right_side_word(word: list[Any], markers: tuple[float, float, float, float], extra_margin) -> bool:
    """
    True if the word's right edge (x1) is near the marker right boundary (validx1),
    within p.VARIANCE (+ optional extra margin).
    """
    x1 = float(word[2])
    validx1 = float(markers[2])
    return (validx1 - (p.VARIANCE + extra_margin)) < x1 < (validx1 + (p.VARIANCE + extra_margin))


def _pick_amount_word(
    transaction_words: list[list[Any]],
    markers: tuple[float, float, float, float],
) -> tuple[Status, float | str, str | None, list[Any] | None]:
    """
    Choose the best amount candidate on the right side of the transaction.

    Returns:
        (status, amount_value, ttype, chosen_word)
    """
    validx1 = float(markers[2])

    best_word: list[Any] | None = None
    best_status: Status = Status.NONE
    best_amount: float | str = "0"
    best_type: str | None = None
    best_dist: float = 10**9

    for w in transaction_words:
        # Only consider right-side-ish words (amount is on the right)
        if not _is_right_side_word(w, markers, extra_margin=p.EXTRA_MARGIN):
            continue

        st, val, ttype = amount_type_per_item(w, markers)

        # We only care about TRUE candidates here (your amount validator is strict)
        if st != Status.TRUE:
            continue

        # choose closest x1 to right boundary
        x1 = float(w[2])
        dist = abs(x1 - validx1)

        if dist < best_dist:
            best_dist = dist
            best_word = w
            best_status = st
            best_amount = val
            best_type = ttype

    return best_status, best_amount, best_type, best_word

def _normalize_money_token(raw: str) -> str | None:
    """
    Normalize common bank-statement money formats to a python-float-friendly string.

    Returns normalized string (e.g. "-2211.46") or None if it doesn't look like money.
    """
    if raw is None:
        return None

    s = str(raw).strip().replace(" ", "")

    # Trailing minus (common in statements): "415,10-" -> "-415,10" (optional, but doesnt hurt)
    if s.endswith("-") and not s.startswith("-"):
        s = "-" + s[:-1]

    # Failsafe: leading plus handling like "123,45+" (rare)
    if s.endswith("+") and not s.startswith("+"):
        s = "+" + s[:-1]

    # EU thousands format: 1.234,56
    if p._THOUSANDS_EU.match(s):
        s = s.replace(".", "").replace(",", ".")
        return s

    # Plain EU decimal: 1234,56 or -1234,56
    if p._MONEY_EU.match(s):
        s = s.replace(",", ".")
        return s

    # Already float-friendly? allow "2211.46" too
    if re.match(r"^\s*[-+]?\d+(\.\d+)?\s*$", s):
        return s

    return None

def _pick_date_word(
    transaction_words: list[list[Any]],
    amount_word: list[Any] | None,
    markers: tuple[float, float, float, float],
    yr: str | None,
) -> tuple[Status, str, list[Any] | None]:
    """
    Choose the best date candidate (DDMM).

    New logic:
    - Prefer same line as amount (then neighbor lines)
    - Date is typically LEFT of the amount
    - Choose the DDMM token closest to the amount in x-distance
    """
    if amount_word is None:
        return Status.NONE, "0", None

    amount_line = int(amount_word[6])
    amount_x0 = float(amount_word[0])  # left edge of amount token

    preferred_lines = (amount_line, amount_line - 1, amount_line + 1)

    best_word: list[Any] | None = None
    best_status: Status = Status.NONE
    best_date: str = "0"
    best_dist: float = 10**9

    for ln in preferred_lines:
        for w in transaction_words:
            if int(w[6]) != ln:
                continue

            txt = str(w[4]).strip()

            # quick filter: date token is usually 4 digits DDMM
            if not (txt.isdigit() and len(txt) == 4):
                continue

            # date should be left of the amount (allow tiny overlap margin)
            w_x1 = float(w[2])
            if w_x1 > amount_x0 + p.VARIANCE:
                continue

            st, date_val = date_per_item(w, amount_word, yr)

            # Score by closeness to amount in x-direction
            dist = abs(amount_x0 - w_x1)

            if st == Status.TRUE:
                # pick closest TRUE
                if dist < best_dist or best_status != Status.TRUE:
                    best_status = st
                    best_date = date_val
                    best_word = w
                    best_dist = dist

            elif st == Status.PARTIAL and best_status != Status.TRUE:
                if dist < best_dist or best_status != Status.PARTIAL:
                    best_status = st
                    best_date = date_val
                    best_word = w
                    best_dist = dist

        # If we already found a TRUE date on the same line (ln == amount_line),
        # we can stop early.
        if best_status == Status.TRUE: #and ln == amount_line:
            return best_status, best_date, best_word

    return best_status, best_date, best_word


def _pick_name_from_words(transaction_words: list[list[Any]]) -> tuple[Status, str]:
    """
    Use your existing name pipeline on the provided word list.
    """
    cleaned = name_main(transaction_words)
    if not cleaned:
        return Status.FALSE, "unknown"

    best = name_scoring_main(cleaned)
    if not best:
        return Status.FALSE, "unknown"

    return Status.TRUE, best


def map_transaction(
    transaction_words: list[list[Any]],
    markers: tuple[float, float, float, float],
    yr: str | None = None,
) -> tuple[dict[str, Any], dict[str, Status]]:
    """
    Map ONE transaction (list of word rows) into your schema dict + field statuses.

    Returns:
        (tx_dict, status_dict)
    """
    # 1) Amount + type
    amount_status, amount_val, ttype, amount_word = _pick_amount_word(transaction_words, markers)
    print("amount")
    print(amount_val)
    print()

    # 2) Date
    date_status, date_val, date_word = _pick_date_word(transaction_words, amount_word, markers, yr)
    print("date")
    print(date_val)
    print()
    

    # 3) Remove amount/date words from the input before name detection
    remaining = _remove_words(transaction_words, [amount_word, date_word])

    # 4) Name on remaining
    name_status, name_val = _pick_name_from_words(remaining)

    # 5) Build transaction dict (category placeholder for now)
    try:
        amount_numeric = float(amount_val)
    except (TypeError, ValueError):
        amount_numeric = 0.0

    tx: dict[str, Any] = {
        "name": name_val,
        "category": "unknown",
        "type": ttype if ttype else TRANSACTION_TYPES[0],
        "amount": amount_numeric,
        "date": date_val if date_status in (Status.TRUE, Status.PARTIAL) else DEFAULT_DATE,
    }

    # 6) Field statuses
    status: dict[str, Status] = {
        "name": name_status,
        "amount": amount_status,
        "type": amount_status if ttype else Status.FALSE,
        "date": date_status,
    }

    return tx, status



def name_main(transaction):
    per_line_list = _name_item_formatter(transaction)

    cleaned = _name_filter(per_line_list)

    return cleaned


def _is_between(x, validx, variance) -> bool:
    return (validx - variance) < x < (validx + variance)
