"""Hub for creating or loading saves."""
import core.core_config as core_config

import cli.helper as h
import cli.prettyprint as pp
import cli.prompts as pr


def prehub(choice, engine):
    pp.clearterminal()
    pp.highlight(pr.PREHUB_NAME)

    max_fails = core_config.AMOUNT_OF_CONSECUTIVE_PREHUB_FAILS
    load_failures = 0

    while True:
        if choice == 1:  # Load save
            print(pr.LOADING_SAVE)
            load_res = engine.load_state()
            if not load_res.ok or not isinstance(load_res.data, tuple) or len(load_res.data) != 2:
                status, save = None, None
            else:
                status, save = load_res.data

            engine.clear_redo_stack()
            engine.clear_undo_stack()

            if status is True:  # success
                load_failures = 0
                return save

            if status is False:
                pp.highlight(pr.NO_SAVE_DETECTED)
            elif status is None:
                pp.highlight(pr.FILE_CORRUPTED)
            else:
                pp.highlight(pr.UNKNOWN_LOAD_STATE)  # failsafe

            load_failures += 1
            if load_failures > max_fails: # Too many fails
                raise SystemExit(pr.PREHUB_TOO_MANY_FAILS)

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

            status_res = engine.restore_latest_backup()
            status = status_res.data if status_res.ok else None

            if status is True:
                pp.highlight(pr.BACKUP_REINSTATED)
                # Load the restored save now and return
                load_res = engine.load_state()
                if not load_res.ok or not isinstance(load_res.data, tuple) or len(load_res.data) != 2:
                    status2, save2 = None, None
                else:
                    status2, save2 = load_res.data
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
            save = cr_new_save(engine)
            if save is None:
                return None
            load_failures = 0
            return save

        else:
            raise SystemExit(pr.PREHUB_INVALID_INITIAL_CHOICE)

def cr_new_save(engine):
    print()
    print(f"{pr.CR_SAVE}")
    save = cr_save_loop(pr.CR_SAVE_NAME)
    if save is None:
        return None
    
    save_result = engine.save_state(save)

    if not save_result.ok or save_result.data is not True:
        pp.highlight(pr.FAILED_TO_WRITE_SAVE)
        return None
    print()
    print(f"{pr.LD_SAVE}")
    return save


def cr_save_loop(prompt_label):
    transactions, definers, _, count = core_config.initvars()

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
    suffix = list(pr.ITEM_SUFFIXES)
    if count < 3:
        print(f"{count+1}{suffix[count]} {pr.ITEM_LABEL}:")
    else:
        print(f"{count+1}{suffix[3]} {pr.ITEM_LABEL}:")

    item = {}

    for name, dtype in definers:
        while True:
            prompt_label = f"{name.capitalize()}, {dtype.__name__}"
            if name == "date":
                prompt_label = f"{name.capitalize()} ({pr.DATE_FORMAT_HUMAN}), {dtype.__name__}"

            raw = pp.pinput(f"{prompt_label}: ")

            value = h.validate_entry(name, raw)
            if value is None:
                continue

            item[name] = value
            break

    count += 1
    return item, count
