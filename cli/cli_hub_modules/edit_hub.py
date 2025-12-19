"""Hub for editing transactions."""
import copy

import core.core_config as core_config

import cli.helper as h
import cli.prettyprint as pp
import cli.prompts as pr

from cli.cli_hub_modules.prehub import cr_save_loop


def _is_snapshot_error(result):
    return isinstance(result.error, RuntimeError) and str(result.error) == "undo snapshot failed"


def _maybe_session_backup(engine, save, session_backup_done):
    if session_backup_done:
        return session_backup_done

    backup_res = engine.session_backup(save)
    if backup_res.ok and backup_res.data is True:
        return True
    return False


def edit_hub(save, engine, session_backup_done):
    snapshot_done = False
    while True:
        pp.clearterminal()
        _, definers, _, _ = core_config.initvars()
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
            return None, session_backup_done, False

        if choice == 1:
            save, session_backup_done, snapshot_done, abort = edit_transaction(
                save,
                definers,
                engine,
                session_backup_done,
                snapshot_done,
            )
            if abort:
                return save, session_backup_done, True
            return save, session_backup_done, False

        if choice == 2:
            save, session_backup_done, snapshot_done, abort = delete_transaction(
                save,
                engine,
                session_backup_done,
                snapshot_done,
            )
            if abort:
                return save, session_backup_done, True
            return save, session_backup_done, False

        if choice == 3:
            save, session_backup_done, snapshot_done, abort = add_transaction(
                save,
                engine,
                session_backup_done,
                snapshot_done,
            )
            if abort:
                return save, session_backup_done, True
            return save, session_backup_done, False

        if choice == 4:
            pp.listnesteddict(save)
            pp.pinput(pr.INPUT_ANY)
            continue

        raise SystemExit(pr.EDIT_HUB_INVALID_CHOICE)


def edit_transaction(save, definers, engine, session_backup_done, snapshot_done):
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
        return None, session_backup_done, snapshot_done, False

    item_index = choice
    item = copy.deepcopy(save[choice - 1])
    print(pr.SELECTED_ITEM_LABEL)
    print(pr.ITEM_NUMBER_LABEL.format(index=choice))

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
            return None, session_backup_done, snapshot_done, False

        selected_key = definers[key_choice - 1][0]
        print(pr.SELECTED_KEY_LABEL.format(key=selected_key.capitalize()))
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
            if not snapshot_done:
                session_backup_done = _maybe_session_backup(engine, save, session_backup_done)

            edit_res = engine.edit_transaction(
                item_index - 1,
                new_tx=item,
                snapshot=not snapshot_done,
            )
            if not edit_res.ok:
                if _is_snapshot_error(edit_res):
                    pp.highlight(pr.UNDO_BACKUP_FAILED)
                    if not h.ask_yes_no(f"{pr.CONTINUE_WITHOUT_UNDO_BACKUP} {pr.YN}"):
                        return save, session_backup_done, snapshot_done, True
                    edit_res = engine.edit_transaction(item_index - 1, new_tx=item, snapshot=False)

                if not edit_res.ok:
                    pp.highlight(pr.FAILED_SAVE_CHANGES)
                    return save, session_backup_done, snapshot_done, True

            snapshot_done = True
            return edit_res.data, session_backup_done, snapshot_done, False

        return None, session_backup_done, snapshot_done, False


def delete_transaction(save, engine, session_backup_done, snapshot_done):
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
            if deleted_any:
                return save, session_backup_done, snapshot_done, False
            return None, session_backup_done, snapshot_done, False

        item = save[choice - 1]
        print(pr.SELECTED_ITEM_FOR_DELETION.format(index=choice))
        pp.listdict(item)

        if not h.ask_yes_no(f"{pr.WOULDYOU_PROCEED_PROMPT} {pr.YN}"):
            if h.ask_yes_no(f"{pr.RETRY_DEL_PROMPT} {pr.YN}"):
                continue
            if deleted_any:
                return save, session_backup_done, snapshot_done, False
            return None, session_backup_done, snapshot_done, False

        if not snapshot_done:
            session_backup_done = _maybe_session_backup(engine, save, session_backup_done)

        del_res = engine.delete_transaction(choice - 1, snapshot=not snapshot_done)
        if not del_res.ok:
            if _is_snapshot_error(del_res):
                pp.highlight(pr.UNDO_BACKUP_FAILED)
                if not h.ask_yes_no(f"{pr.CONTINUE_WITHOUT_UNDO_BACKUP} {pr.YN}"):
                    return save, session_backup_done, snapshot_done, True
                del_res = engine.delete_transaction(choice - 1, snapshot=False)

            if not del_res.ok:
                pp.highlight(pr.FAILED_SAVE_CHANGES)
                return save, session_backup_done, snapshot_done, True

        save = del_res.data
        snapshot_done = True
        deleted_any = True

        if not save:
            print(pr.NO_MORE_TRANSACTIONS)
            return save, session_backup_done, snapshot_done, False

        if not h.ask_yes_no(f"{pr.DEL_ANOTHER_PROMPT} {pr.YN}"):
            return save, session_backup_done, snapshot_done, False


def add_transaction(save, engine, session_backup_done, snapshot_done):
    addition = cr_save_loop(pr.ADD_TRANSACTION_PROMPT)
    if addition is None:
        return None, session_backup_done, snapshot_done, False

    for idx, item in enumerate(addition):
        if not snapshot_done:
            session_backup_done = _maybe_session_backup(engine, save, session_backup_done)

        add_res = engine.add_transaction(item, snapshot=not snapshot_done)
        if not add_res.ok:
            if _is_snapshot_error(add_res):
                pp.highlight(pr.UNDO_BACKUP_FAILED)
                if not h.ask_yes_no(f"{pr.CONTINUE_WITHOUT_UNDO_BACKUP} {pr.YN}"):
                    return save, session_backup_done, snapshot_done, True
                add_res = engine.add_transaction(item, snapshot=False)

            if not add_res.ok:
                pp.highlight(pr.FAILED_SAVE_CHANGES)
                return save, session_backup_done, snapshot_done, True

        save = add_res.data
        snapshot_done = True

    return save, session_backup_done, snapshot_done, False
