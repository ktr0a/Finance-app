""""""
import copy

import core.core_config as core_config

import cli.helper as h
import cli.prettyprint as pp
import cli.prompts as pr




def undoredo_hub(save, engine):
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
            undo_res = engine.undo()
            if not undo_res.ok or not isinstance(undo_res.data, tuple) or len(undo_res.data) != 2:
                ok, new_save = None, None
            else:
                ok, new_save = undo_res.data
            if not ok or new_save is None:
                pp.highlight(pr.NOTHING_TO_UNDO)
                pp.pinput(pr.INPUT_ANY)
                continue

            save = new_save
            pp.highlight(pr.ACTION_UNDONE)
            pp.pinput(pr.INPUT_ANY)

        elif choice == 2:  # redo
            redo_res = engine.redo()
            if not redo_res.ok or not isinstance(redo_res.data, tuple) or len(redo_res.data) != 2:
                ok, new_save = None, None
            else:
                ok, new_save = redo_res.data
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



