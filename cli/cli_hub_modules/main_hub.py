"""General hub routing to other hubs."""
import time

import core.storage as s

import cli.helper as h
import cli.prettyprint as pp
import cli.prompts as pr

from cli.cli_hub_modules.analyze_hub import analyze_hub
from cli.cli_hub_modules.calc_hub import calc_hub
from cli.cli_hub_modules.edit_hub import edit_hub


def hub(save):
    print(pr.SAVE_LOADED)
    time.sleep(1)
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
            edited_save = edit_hub(save)
            if edited_save is not None:
                save = edited_save
                s.save(save)

        else:
            raise SystemExit("hub: invalid choice")
