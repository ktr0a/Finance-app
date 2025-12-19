"""Hub for filtering data before calculations."""
from finance_app.core import core_config

import finance_app.cli.helper as h
import finance_app.cli.prettyprint as pp
import finance_app.cli.ui.text as pr


def analyze_hub(save, engine):
    _, definers, _, _ = core_config.initvars()

    pp.clearterminal()
    pp.highlight(pr.AHUB_NAME)
    print()
    print(pr.AHUB_PROMPT)
    print()
    pp.listoptions(pr.AHUB_OPTIONS)
    print(f"0. {pr.EXIT}")
    print()

    while True:
        choice_str = pp.pinput(pr.ENTER_ACC_NUMBER)
        choice = h.validate_numberinput(choice_str, len(pr.AHUB_OPTIONS), allow_zero=True)
        if choice is not None:
            break

    if choice == 0:
        return None

    if choice == 1:
        return save

    if choice == 2:
        return filter_save(save, definers, engine)

    raise SystemExit(pr.ANALYZE_HUB_INVALID_CHOICE)


def filter_save(save, definers, engine):
    if not save:
        print(pr.SAVE_IS_EMPTY)
        return None

    while True:
        _, definers, _, _ = core_config.initvars()

        pp.clearterminal()
        pp.highlight(pr.FILTER_NAME)
        print()
        print(pr.FILTER_PROMPT_KEY)
        print()
        pp.listnested(definers)
        print()

        while True:
            choice_str = pp.pinput(pr.ENTER_ACC_NUMBER)
            choice = h.validate_numberinput(choice_str, len(definers))
            if choice is not None:
                filterby_key = definers[choice - 1][0]
                break

        pp.clearterminal()
        pp.highlight(pr.FILTER_NAME)
        print()
        print(pr.FILTERING_BY_LABEL.format(field=filterby_key))
        print()

        while True:
            choice_str = pp.pinput(pr.FILTER_PROMPT_VALUE)
            choice = h.validate_entry(filterby_key, choice_str)
            if choice is not None:
                filterby_value = choice
                break

        pp.clearterminal()
        pp.highlight(pr.FILTER_NAME)
        print()
        print(f"\n{pr.FILTERING_BY_VALUE_LABEL.format(field=filterby_key.capitalize(), value=filterby_value)}")
        print()

        filtered_res = engine.filter_transactions(filterby_key, filterby_value, save)
        if not filtered_res.ok:
            return None
        filtered_save = filtered_res.data

        if not filtered_save:
            print(pr.SELECTION_NOT_FOUND.format(key=filterby_key, value=filterby_value))
            if h.ask_yes_no(f"{pr.RETRY_PROMPT} {pr.YN}"):
                continue
            return None

        pp.listnesteddict(filtered_save)
        if h.ask_yes_no(f"{pr.USE_FILTERED_DATASET} {pr.YN}") is True:
            break

        if h.ask_yes_no(f"{pr.RETRY_FILTER} {pr.YN}") is True:
            continue

        return None

    return filtered_save



