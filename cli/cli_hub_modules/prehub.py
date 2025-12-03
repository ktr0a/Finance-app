"""Hub for creating or loading saves."""
import core.config as config
import core.storage as s

import cli.helper as h
import cli.prettyprint as pp
import cli.prompts as pr


def prehub(choice):
    """Handle save loading or creation based on the initial choice."""
    pp.clearterminal()
    pp.highlight(pr.PREHUB_NAME)

    if choice == 0:
        return None

    if choice == 1:
        print(pr.LOADING_SAVE)

        try:
            save = s.load()
        except Exception:
            print(pr.FILE_CORRUPTED)
            if h.ask_yes_no(f"{pr.CR_NEW_SAVE_INSTEAD} {pr.YN}"):
                return cr_new_save()
            return None

        if not save:
            print(pr.NO_SAVE_DETECTED)
            if h.ask_yes_no(f"{pr.CR_NEW_SAVE_INSTEAD} {pr.YN}"):
                return cr_new_save()
            return None

        return save

    if choice == 2:
        save = cr_new_save()
        if save is None:
            return None
        return save

    raise SystemExit("prehub: invalid initial choice")


def cr_new_save():
    print()
    print(f"{pr.CR_SAVE}")
    save = cr_save_loop(pr.CR_SAVE_NAME)
    if save is None:
        return None
    s.save(save)
    print()
    print(f"{pr.LD_SAVE}")
    return save


def cr_save_loop(prompt_label):
    transactions, definers, _, count = config.initvars()

    pp.clearterminal()
    pp.highlight(prompt_label)
    print()
    print(pr.CR_SAVE_LOOP_PROMPT)
    print()
    pp.listnested(definers)
    print()

    if not h.ask_yes_no(f"{pr.WOULDYOU_PROCEED_PROMPT} {pr.YN}"):
        return None

    while True:
        item, count = item_loop(definers, count)
        transactions.append(item)

        print()
        print(pr.SUCCESSFULLY_ADDED)
        for key, value in item.items():
            print(f"  {key.capitalize():<10}: {value}")
        print()

        if not h.ask_yes_no(f"{pr.ADD_ANOTHER_PROMPT} {pr.YN}"):
            break

    return transactions


def item_loop(definers, count):
    pp.clearterminal()
    suffix = ["st", "nd", "rd", "th"]
    if count < 3:
        print(f"{count+1}{suffix[count]} Item:")
    else:
        print(f"{count+1}{suffix[3]} Item:")

    item = {}

    for name, dtype in definers:
        while True:
            prompt_label = f"{name.capitalize()}, {dtype.__name__}"
            if name == "date":
                prompt_label = f"{name.capitalize()} (DD.MM.YYYY), {dtype.__name__}"

            raw = pp.pinput(f"{prompt_label}: ")

            value = h.validate_entry(name, raw)
            if value is None:
                continue

            item[name] = value
            break

    count += 1
    return item, count
