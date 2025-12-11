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
    
    if _is_between(x1, validx1, p.VARIANCE) is None:
        return (Status.NONE, "0", None)
    
    definers = _initdefiners()
    akey = definers[3][0]

    value = h.validate_entry(akey, text)

    if value is None: # is amount valid
        return (Status.FALSE, "1", None)
    
    if text.strip()[-1:] == "-":
        ttype = TRANSACTION_TYPES[1]
    else: ttype = TRANSACTION_TYPES[0]

    
    return (Status.TRUE, value, ttype)

# 2nd to last item of 1st line
def date_per_item(dateword: list, amountword: list, yr: str | None = None) -> tuple[Status, str]:

    x0, y0, x1, y1, text, block_no, line_no, word_no = dateword
    validx0, validy0, validx1, validy1, *_ = amountword

    text = text.strip()
    print(text)

    # Item doesnt quality
    if _is_between(y0, validy0, p.VARIANCE) and _is_between(y1, validy1, p.VARIANCE) is None:
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

            # Pure integers 
            try: int(w); continue
            except ValueError: pass

            newline.append(w)

        if newline: # Dedupe (perline and overall)
            newline = _name_dedupe_words_in_line(newline) 
            line_key = tuple(newline)

            if line_key not in seen_lines:
                seen_lines.add(line_key)
                cleaned.append(newline)

    cleaned = _name_remove_subset_lines(cleaned)

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

def _name_remove_subset_lines(lines: list[list[str]]) -> list[list[str]]:
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


def name_main(transaction):
    per_line_list = _name_item_formatter(transaction)

    cleaned = _name_filter(per_line_list)

    flattened = _name_flatten_lst(cleaned if cleaned is not None else exit("cleaned is none"))

    return flattened






def _is_between(x, validx, variance) -> bool:
    return (validx - variance) < x < (validx + variance)