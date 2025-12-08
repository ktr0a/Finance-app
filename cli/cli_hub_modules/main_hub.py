"""General hub routing to other hubs."""
import time
import copy

import core.storage as s

import cli.helper as h
import cli.prettyprint as pp
import cli.prompts as pr

from cli.cli_hub_modules.analyze_hub import analyze_hub
from cli.cli_hub_modules.calc_hub import calc_hub
from cli.cli_hub_modules.edit_hub import edit_hub
from cli.cli_hub_modules.undoredo_hub import undoredo_hub



def hub(save):
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
            new_save = analyze_hub(save)
            if new_save is None:
                continue
            calc_hub(new_save)

        elif choice == 2:
            pp.listnesteddict(save)
            pp.pinput(pr.INPUT_ANY)

        elif choice == 3:
            old_save = copy.deepcopy(save)

            edited_save = edit_hub(save)

            if edited_save is None:
                print('1')
                pp.pinput(pr.INPUT_ANY)
                continue

            if edited_save == old_save:
                pp.highlight("No changes made.")
                pp.pinput(pr.INPUT_ANY)
                continue

            if not session_backup_done:
                save_status = s.edit_and_backup_save(old_save) # backup current save
                if save_status is True:
                    session_backup_done = True

            
            status = s.cr_backup_lst(old_save, mode='undo', delbackup=False) # backup current save to undo stack
            if status is not True:
                pp.highlight("Undo Backup failed")
                if not h.ask_yes_no(f"Continue without undo backup? {pr.YN}"):
                    continue

            save_status = s.save(edited_save)
            s.clear_redo_stack()

            if save_status is not True:
                pp.highlight("Failed to save changes to disk.")
                continue

            save = edited_save

        elif choice == 4:
            status = s.cr_backup_lst(save)
            if status is True:
                pp.highlight("Backup created.")
                session_backup_done = True
            else:
                pp.highlight(pr.BACKUP_FAILED)
            pp.pinput(pr.INPUT_ANY)

        elif choice == 5:
            restored_save = _restore_backup_flow()
            if restored_save is not None:
                save = restored_save
                session_backup_done = False

        elif choice == 6:
            save = undoredo_hub(save)



        else:
            raise SystemExit("hub: invalid choice")


def _restore_backup_flow():
    backups = s.list_backups()
    if not backups:
        pp.highlight(pr.NO_BACKUPS_FOUND)
        pp.pinput(pr.INPUT_ANY)
        return None

    while True:
        pp.clearterminal()
        pp.highlight("Restore backup")
        print()
        print("Select a backup to restore:")
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
        restore_status = s.restore_backup_file(target)

        if restore_status is None:
            pp.highlight("Selected backup is unreadable.")
            pp.pinput(pr.INPUT_ANY)
            continue

        if restore_status is False:
            pp.highlight(pr.BACKUP_FAILED)
            pp.pinput(pr.INPUT_ANY)
            return None

        cleanup_error = _delete_all_backups(backups)
        status, new_save = s.load()

        if status is not True:
            pp.highlight("Backup restored but failed to reload save from disk.")
            return None

        pp.highlight(pr.BACKUP_REINSTATED)
        if cleanup_error:
            pp.highlight("Warning: Failed to delete one or more backups.")

        pp.pinput(pr.INPUT_ANY)
        return new_save


def _delete_all_backups(backups):
    cleanup_error = False
    for backup in backups:
        if not backup.exists():
            continue
        try:
            backup.unlink()
        except OSError:
            cleanup_error = True
    return cleanup_error
