from pathlib import Path

try:
    import pdf_handeling.rawdata as rawdata
except ImportError:
    import rawdata


ROUNDING_INT = rawdata.ROUNDING_INT
MARKER_STR = rawdata.MARKER_STR
BLACKLIST = rawdata.BLACKLIST
CATEGORY_VARIANCE = rawdata.CATEGORY_VARIANCE
RAWDATA_DIR = rawdata.RAWDATA_DIR
FINAL_DIR = rawdata.FINAL_DIR


def _rounding_values(word: tuple) -> list:
    x0, y0, x1, y1, text, block_no, line_no, word_no = word
    return [
        round(x0, ROUNDING_INT), round(y0, ROUNDING_INT),
        round(x1, ROUNDING_INT), round(y1, ROUNDING_INT),
        text, block_no, line_no, word_no
    ]


def extract_markers(total_wordlst: list, MARKER_STR) -> tuple | None:
    page1 = total_wordlst[0]
    for word in page1:
        x0, y0, x1, y1, text, block_no, line_no, word_no = word
        if text == MARKER_STR:
            return (x0, y0, page1[-1][2], page1[-1][3])
        else:
            continue

    return None


def extract_words_in_markers(total_wordlst: list, markers: tuple) -> list:
    validx0, validy0, validx1, validy1 = markers

    valid_lst = []

    for page in total_wordlst:
        valid_pagelst = []
        for word in page:
            x0, y0, x1, y1, text, block_no, line_no, word_no = word
            if (
                x0 >= validx0 and
                y0 >= validy0 and
                x1 <= validx1 and
                y1 <= validy1
            ):
                valid_pagelst.append(word)
            else:
                continue

        valid_lst.append(valid_pagelst)

    return valid_lst


def sort_to_transactions(valid_lst: list, markers: tuple) -> list:
    transactions_lst = []
    validx0, validy0, validx1, validy1 = markers

    first_item = True
    item = []

    newvalid_lst = _flatten_lst(valid_lst)
    valid_lst = newvalid_lst

    for idx, word in enumerate(valid_lst):
        x0, y0, x1, y1, text, block_no, line_no, word_no = word

        if _is_between(x0, validx0, CATEGORY_VARIANCE):
            if first_item is True:
                item.append(word)
                first_item = False
            else:
                transactions_lst.append(item)
                item = []
                item.append(word)
        else:
            item.append(word)

    transactions_lst.append(item)

    return transactions_lst


def _is_between(x, validx, variance) -> bool:
    return (validx - variance) < x < (validx + variance)


def _flatten_lst(valid_lst: list) -> list:
    newvalid_lst = []
    for page in valid_lst:
        newvalid_lst.extend(page)
    return newvalid_lst


def delete_blacklist(transactions_lst: list) -> list:
    cleaned = []
    for transaction in transactions_lst:
        has_blacklisted_word = any(word[4] in BLACKLIST for word in transaction)
        if not has_blacklisted_word:
            cleaned.append(transaction)
    return cleaned


def pretty_print_transactions(transactions: list) -> None:
    """
    transactions: list[list[word_tuple]]
    word_tuple = [x0, y0, x1, y1, text, block_no, line_no, word_no]
    """
    for t_idx, tx in enumerate(transactions, start=1):
        print(f"\n================ TRANSACTION {t_idx} ================")
        print(f"(words: {len(tx)})")

        # group by line_no for readability
        lines: dict[int, list[tuple[int, str, float, float, float, float]]] = {}

        for x0, y0, x1, y1, text, block_no, line_no, word_no in tx:
            lines.setdefault(line_no, []).append((word_no, text, x0, y0, x1, y1))

        for line_no in sorted(lines.keys()):
            line_words = sorted(lines[line_no], key=lambda w: w[0])
            line_text = " ".join(w[1] for w in line_words)
            print(f"  line {line_no:3d}: {line_text}")

        # optional: uncomment if you also want raw tuples for each transaction
        # for w in tx:
        #     print("   ", w)


def initpath() -> tuple:
    if RAWDATA_DIR.parent.mkdir(parents=True, exist_ok=True) and FINAL_DIR.parent.mkdir(parents=True, exist_ok=True) is True:
        return (RAWDATA_DIR, FINAL_DIR)


def hastext() -> (bool | None):
    pass

    for page_number, total_words_on_page in enumerate(total_wordlst, start=1):
        print(f"Page: {page_number}")
        for word in total_words_on_page:
            print(f"{word}")

    print()
    markers = extract_markers(total_wordlst, MARKER_STR)
    print(markers)
    print()

    for page_number, total_words_on_page in enumerate(valid_lst, start=1):
        print(f"Page: {page_number}")
        for word in total_words_on_page:
            print(f"{word}")

    print()
    print()
    print()
    print()
    print()
