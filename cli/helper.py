# Helper functions for cli
import core.config as config
import core.storage as s
import cli.prettyprint as pp

def ask_yes_no(prompt) -> bool:
    while True:
        choice = input(f"{prompt}\n").upper().strip()
        if choice in ("Y", "YES"):
            return True
        elif choice in ("N", "NO"):
            return False
        else:
            pp.highlight("Please enter y/n.")

def validate_numberinput(choice_str, max_index):
    choice_str = choice_str.strip()
    if not choice_str.isdigit():
        pp.highlight("Please enter a number")
        return None

    num = int(choice_str)

    if not (1 <= num <= max_index):
        pp.highlight("Invalid choice. Try again.")
        return None

    return num

def validate_entry(key, raw_input):
    _, definers, _, _ = config.initvars()
    raw = raw_input.strip()
    
    var = [t for dkey, t in definers if dkey == key]

    if not var:
        print(f"ERROR: Unknown field '{key}'.")
        return None

    dtype = var[0]

    if key == "category":
        raw = raw.lower()

    if key == "type":
        raw = raw.upper()
        if raw not in ("I", "E"):
            print("ERROR: Type must be I or E.")
            return None
        return raw

    # Special case: AMOUNT
    if key == "amount":
        raw = raw.replace("-", " ")
        raw = raw.replace(",", ".")

    # General datatype conversion
    try:
        value = dtype(raw)
    except ValueError :
        print(f"ERROR: Expected {dtype.__name__}.")
        return None

    return value

