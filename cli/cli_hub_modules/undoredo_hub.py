""""""
import copy

import core.core_config as core_config
import core.storage as s

import cli.helper as h
import cli.prettyprint as pp
import cli.prompts as pr




def undoredo_hub(save):
    while True:
        pp.clearterminal()
        pp.highlight(pr.UNDOREDO_HUB_NAME)
        print()
        print(pr.WOULDYOU_PROMPT)
        print()
        pp.listoptions(pr.UNDOREDO_HUB_OPTIONS)
        print(f"0. {pr.EXIT}")
        print()

        while True:
            choice_str = pp.pinput(pr.ENTER_ACC_NUMBER)
            choice = h.validate_numberinput(choice_str, len(pr.UNDOREDO_HUB_OPTIONS), allow_zero=True)
            if choice is not None:
                break

        if choice == 0:
            return save
        
        if choice == 1:  # undo
            ok, new_save = s.undo_action()
            if not ok or new_save is None:
                pp.highlight(pr.NOTHING_TO_UNDO)
                pp.pinput(pr.INPUT_ANY)
                continue

            save = new_save
            pp.highlight(pr.ACTION_UNDONE)
            pp.pinput(pr.INPUT_ANY)

        elif choice == 2:  # redo
            ok, new_save = s.redo_action()
            if not ok or new_save is None:
                pp.highlight(pr.NOTHING_TO_REDO)
                pp.pinput(pr.INPUT_ANY)
                continue

            save = new_save
            pp.highlight(pr.ACTION_REDONE)
            pp.pinput(pr.INPUT_ANY)

        if choice == 3:
            pp.listnesteddict(save)
            pp.pinput(pr.INPUT_ANY)
            continue



