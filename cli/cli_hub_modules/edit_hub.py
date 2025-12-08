"""Hub for editing transactions."""
import copy

import core.config as config

import cli.helper as h
import cli.prettyprint as pp
import cli.prompts as pr

from cli.cli_hub_modules.prehub import cr_save_loop


def edit_hub(save):
    while True:
        pp.clearterminal()
        _, definers, _, _ = config.initvars()
        pp.highlight(pr.EDIT_HUB_NAME)
        print()
        print(pr.WOULDYOU_PROMPT)
        print()
        pp.listoptions(pr.EDIT_HUB_OPTIONS)
        print(f"0. {pr.EXIT}")
        print()

        while True:
            choice_str = pp.pinput(pr.ENTER_ACC_NUMBER)
            choice = h.validate_numberinput(choice_str, len(pr.EDIT_HUB_OPTIONS), allow_zero=True)
            if choice is not None:
                break

        if choice == 0:
            return None

        if choice == 1:
            return edit_transaction(save, definers)

        if choice == 2:
            return delete_transaction(save)

        if choice == 3:
            return add_transaction(save)

        if choice == 4:
            pp.listnesteddict(save)
            pp.pinput(pr.INPUT_ANY)
            continue

        raise SystemExit("edit_hub: invalid choice")


def edit_transaction(save, definers):
    pp.listnesteddict(save)
    print()
    print(pr.EDIT_TRANSACTION_PROMPT)
    print(f"0. {pr.EXIT}")
    print()

    while True:
        choice_str = pp.pinput(pr.ENTER_ACC_NUMBER)
        choice = h.validate_numberinput(choice_str, len(save), allow_zero=True)
        if choice is not None:
            break

    if choice == 0:
        return None

    item_index = choice
    item = copy.deepcopy(save[choice - 1])
    print(f"Selected Item:\nItem: {choice}")

    while True:
        pp.listdict(item)
        print()
        print(pr.SEL_ITEM_PROMPT)
        print()
        pp.listnested(definers)
        print(f"0. {pr.EXIT}")
        print()

        while True:
            choice_str = pp.pinput(pr.ENTER_ACC_NUMBER)
            key_choice = h.validate_numberinput(choice_str, len(definers), allow_zero=True)
            if key_choice is not None:
                break

        if key_choice == 0:
            return None

        selected_key = definers[key_choice - 1][0]
        print(f"Selected key: {selected_key.capitalize()}")
        print()

        while True:
            raw = pp.pinput(f"{pr.NEW_VALUE_PROMPT}: ")
            value = h.validate_entry(selected_key, raw)
            if value is None:
                continue
            break

        item[selected_key] = value

        pp.listdict(item)

        if h.ask_yes_no(f"{pr.REDO_EDIT_TRANSACTION_PROMPT} {pr.YN}"):
            continue

        if h.ask_yes_no(f"{pr.ADD_ITEM_TO_SAVE} {pr.YN}"):
            save[item_index - 1] = item
            return save

        return None


def delete_transaction(save):
    deleted_any = False

    while True:
        pp.listnesteddict(save)
        print()
        print(pr.DEL_TRANSACTION_PROMPT)
        print(f"0. {pr.EXIT}")
        print()

        while True:
            choice_str = pp.pinput(pr.ENTER_ACC_NUMBER)
            choice = h.validate_numberinput(choice_str, len(save), allow_zero=True)
            if choice is not None:
                break

        if choice == 0:
            return save if deleted_any else None

        item = save[choice - 1]
        print(f"Selected Item for deletion (Item {choice}):")
        pp.listdict(item)

        if not h.ask_yes_no(f"{pr.WOULDYOU_PROCEED_PROMPT} {pr.YN}"):
            if h.ask_yes_no(f"{pr.RETRY_DEL_PROMPT} {pr.YN}"):
                continue
            return save if deleted_any else None

        save.pop(choice - 1)
        deleted_any = True

        if not save:
            print("No more transactions.")
            return save

        if not h.ask_yes_no(f"{pr.DEL_ANOTHER_PROMPT} {pr.YN}"):
            print(save)
            return save


def add_transaction(save):
    addition = cr_save_loop(pr.ADD_TRANSACTION_PROMPT)
    if addition is None:
        return None

    for item in addition:
        save.append(item)

    return save
