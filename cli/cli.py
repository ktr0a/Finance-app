# Take userinput & give it to storage.py (& utils.py, if applicable).
import cli.helper as h
import cli.prettyprint as pp
import cli.prompts as pr

from cli.cli_hub_modules.main_hub import hub
from cli.cli_hub_modules.prehub import prehub

__all__ = ["start", "hub"]


def start(engine):
    pp.clearterminal()
    pp.highlight(pr.PROGRAM_ON)
    """Run the initial start flow and return a loaded save when successful."""
    while True:
        pp.clearterminal()
        pp.highlight(pr.START)
        print()
        print(pr.WOULDYOU_PROMPT)
        print()
        pp.listoptions(pr.START_OPTIONS)
        print(f"0. {pr.EXIT}")
        print()

        while True:
            choice_str = pp.pinput(pr.ENTER_ACC_NUMBER)
            choice = h.validate_numberinput(choice_str, len(pr.START_OPTIONS), allow_zero=True)
            if choice is not None:
                break

        if choice == 0:
            return None

        save = prehub(choice, engine)

        if save is None:
            # User backed out, so keep looping in the start menu.
            continue

        return save
