"""General hub routing to other hubs."""
import time
import copy

import finance_app.cli.helper as h
import finance_app.cli.prettyprint as pp
import finance_app.cli.ui.text as pr

from finance_app.cli.cli_hub_modules.analyze_hub import analyze_hub
from finance_app.cli.cli_hub_modules.calc_hub import calc_hub
from finance_app.cli.cli_hub_modules.edit_hub import edit_hub
from finance_app.cli.cli_hub_modules.undoredo_hub import undoredo_hub



def hub(save, engine):
    print(pr.SAVE_LOADED)
    time.sleep(1)

    session_backup_done = False

    while True:
        pp.clearterminal()
        pp.highlight(pr.HUB_NAME)
        print()
        print(pr.WOULDYOU_PROMPT)
        print()
        pp.listoptions(pr.HUB_OPTIONS)
        print(f"0. {pr.EXIT}")
        print()

        while True:
            choice_str = pp.pinput(pr.ENTER_ACC_NUMBER)
            choice = h.validate_numberinput(choice_str, len(pr.HUB_OPTIONS), allow_zero=True)
            if choice is not None:
                break

        if choice == 0:
            return None

        if choice == 1:
            new_save = analyze_hub(save, engine)
            if new_save is None:
                continue
            calc_hub(new_save, engine)

        elif choice == 2:
            list_res = engine.list_transactions()
            if list_res.ok and list_res.data is not None:
                save = list_res.data
            pp.listnesteddict(save)
            pp.pinput(pr.INPUT_ANY)

        elif choice == 3:
            old_save = copy.deepcopy(save)

            edited_save, session_backup_done, aborted = edit_hub(
                save,
                engine,
                session_backup_done,
            )

            if aborted:
                continue

            if edited_save is None:
                print(pr.EDIT_HUB_NO_RESULT)
                pp.pinput(pr.INPUT_ANY)
                continue

            if edited_save == old_save:
                pp.highlight(pr.NO_CHANGES_MADE)
                pp.pinput(pr.INPUT_ANY)
                continue

            save = edited_save

        elif choice == 4:
            status_res = engine.create_backup(save)
            if status_res.ok and status_res.data is True:
                pp.highlight(pr.BACKUP_CREATED)
                session_backup_done = True
            else:
                pp.highlight(pr.BACKUP_FAILED)
            pp.pinput(pr.INPUT_ANY)

        elif choice == 5:
            restored_save = _restore_backup_flow(engine)
            if restored_save is not None:
                save = restored_save
                session_backup_done = False

        elif choice == 6:
            save = undoredo_hub(save, engine)



        else:
            raise SystemExit(pr.MAIN_HUB_INVALID_CHOICE)


def _restore_backup_flow(engine):
    backups_res = engine.list_backups()
    backups = backups_res.data if backups_res.ok else []
    if not backups:
        pp.highlight(pr.NO_BACKUPS_FOUND)
        pp.pinput(pr.INPUT_ANY)
        return None

    while True:
        pp.clearterminal()
        pp.highlight(pr.RESTORE_BACKUP_TITLE)
        print()
        print(pr.SELECT_BACKUP_TO_RESTORE)
        print()
        for idx, backup in enumerate(backups, start=1):
            print(f"{idx}. {backup.name}")
        print(f"0. {pr.EXIT}")
        print()

        choice_str = pp.pinput(pr.ENTER_ACC_NUMBER)
        choice = h.validate_numberinput(choice_str, len(backups), allow_zero=True)
        if choice is None:
            continue

        if choice == 0:
            return None

        target = backups[choice - 1]
        restore_res = engine.restore_backup_file(target)
        restore_status = restore_res.data if restore_res.ok else None

        if restore_status is None:
            pp.highlight(pr.SELECTED_BACKUP_UNREADABLE)
            pp.pinput(pr.INPUT_ANY)
            continue

        if restore_status is False:
            pp.highlight(pr.BACKUP_FAILED)
            pp.pinput(pr.INPUT_ANY)
            return None

        cleanup_res = engine.delete_backup_files(backups)
        cleanup_error = cleanup_res.data if cleanup_res.ok else True

        load_res = engine.load_state()
        if not load_res.ok or not isinstance(load_res.data, tuple) or len(load_res.data) != 2:
            status, new_save = None, None
        else:
            status, new_save = load_res.data

        if status is not True:
            pp.highlight(pr.BACKUP_RELOAD_FAILED)
            return None

        pp.highlight(pr.BACKUP_REINSTATED)
        if cleanup_error:
            pp.highlight(pr.WARNING_BACKUP_DELETE)

        pp.pinput(pr.INPUT_ANY)
        return new_save



