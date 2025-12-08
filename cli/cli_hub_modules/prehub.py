"""Hub for creating or loading saves."""
import core.config as config
import core.storage as s

import cli.helper as h
import cli.prettyprint as pp
import cli.prompts as pr


def prehub(choice):
    pp.clearterminal()
    pp.highlight(pr.PREHUB_NAME)

    max_fails = config.AMOUNT_OF_CONSECUTIVE_PREHUB_FAILS
    load_failures = 0

    while True:
        if choice == 1:  # Load save
            print(pr.LOADING_SAVE)
            status, save = s.load()

            s.clear_redo_stack()
            s.clear_undo_stack

            if status is True:  # success
                load_failures = 0
                return save

            if status is False:
                pp.highlight(pr.NO_SAVE_DETECTED)
            elif status is None:
                pp.highlight(pr.FILE_CORRUPTED)
            else:
                pp.highlight("Unknown load state")  # failsafe

            load_failures += 1
            if load_failures > max_fails: # Too many fails
                raise SystemExit("Contact Dev - repeated load failures")

            REMAINING_OPTIONS = pr.START_OPTIONS[1:]
            print()
            print(pr.WOULDYOU_INSTEAD_PROMPT)
            print()
            pp.listoptions(REMAINING_OPTIONS)
            print(f"0. {pr.EXIT}")

            while True:
                choice2_str = pp.pinput(pr.ENTER_ACC_NUMBER)
                choice2 = h.validate_numberinput(choice2_str, len(REMAINING_OPTIONS), allow_zero=True)
                if choice2 is None:
                    continue
                if choice2 == 0:
                    return None
                break

            choice = choice2 + 1  # map trimmed list back to original indices
            # Reset because we're leaving the "load" path
            load_failures = 0
            continue

        elif choice == 2:  # Restore from latest backup
            print(pr.CONFIRM_BACKUP_OVERRIDE)
            if not h.ask_yes_no(pr.WOULDYOU_PROCEED_PROMPT):
                return None

            status = s.restore_latest_backup()

            if status is True:
                pp.highlight(pr.BACKUP_REINSTATED)
                # Load the restored save now and return
                status2, save2 = s.load()
                if status2 is True:
                    load_failures = 0
                    return save2
                # If loading right after restore still fails, escalate via load path:
                choice = 1
                continue

            if status is False:
                pp.clearterminal()
                pp.highlight(pr.BACKUP_FAILED)
            else:  # None
                pp.clearterminal()
                pp.highlight(pr.NO_BACKUPS_FOUND)

            if not h.ask_yes_no(f"{pr.CR_NEW_SAVE_INSTEAD} {pr.YN}"):
                return None

            choice = 3
            load_failures = 0
            continue

        elif choice == 3:  # Create new save
            save = cr_new_save()
            if save is None:
                return None
            load_failures = 0
            return save

        else:
            raise SystemExit("prehub: invalid initial choice")

def cr_new_save():
    print()
    print(f"{pr.CR_SAVE}")
    save = cr_save_loop(pr.CR_SAVE_NAME)
    if save is None:
        return None
    
    save_result = s.save(save)

    if save_result is not True:
        pp.highlight("Failed to write save file.")
        return None
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
