# Helper functions for cli
from datetime import datetime

import cli.prettyprint as pp
import cli.prompts as pr
import core.core_config as core_config
from config.schema import DATE_FORMAT, TRANSACTION_TYPES


def ask_yes_no(prompt) -> bool:
    while True:
        choice = input(f"{prompt}\n").upper().strip()
        if choice in pr.YES_VALUES:
            return True
        elif choice in pr.NO_VALUES:
            return False
        else:
            pp.highlight(pr.YN_PROMPT)


def validate_numberinput(choice_str, max_index, allow_zero = False):
    
    choice_str = choice_str.strip()
    if not choice_str.isdigit():
        pp.highlight(pr.ERROR_ENTER_NUMBER)
        return None

    num = int(choice_str)

    if allow_zero == True:
        if not (0 <= num <= max_index):
            pp.highlight(pr.INVALID_CHOICE)
            return None

    else:
        if not (1 <= num <= max_index):
            pp.highlight(pr.INVALID_CHOICE)
            return None

    return num


def validate_entry(key, raw_input):
    _, definers, _, _ = core_config.initvars()
    raw = raw_input.strip()
    
    var = [t for dkey, t in definers if dkey == key]

    if not var:
        print(pr.ERROR_UNKNOWN_FIELD.format(key=key))
        return None

    dtype = var[0]

    if key == "category":
        raw = raw.lower()

    if key == "type":
        raw = raw.upper()
        if raw not in TRANSACTION_TYPES:
            print(pr.ERROR_TYPE_MUST_BE_IE)
            return None
        return raw

    if key == "date":
        try:
            parsed = datetime.strptime(raw, DATE_FORMAT)
        except ValueError:
            print(pr.ERROR_DATE_FORMAT)
            return None
        # Ensure consistent zero-padded formatting
        return parsed.strftime(DATE_FORMAT)

    # Special case: AMOUNT
    if key == "amount":
        raw = raw.replace("-", " ")
        raw = raw.replace(",", ".")

    # General datatype conversion
    try:
        value = dtype(raw)
    except ValueError :
        print(pr.ERROR_EXPECTED_TYPE.format(dtype=dtype.__name__))
        return None

    return value

