"""Hub for calculations and summaries."""
import cli.helper as h
import cli.prettyprint as pp
import cli.prompts as pr

from cli.cli_hub_modules.summary_hub import summary_hub


def calc_hub(save, engine):
    menu_res = engine.calc_menu()
    c_util = menu_res.data if menu_res.ok else []

    result_list = []
    while True:
        pp.clearterminal()
        pp.highlight(pr.CALC_HUB_NAME)

        if result_list:
            print()
            print(", ".join(result_list))

        print()
        print(pr.CALC_HUB_PROMPT)
        print()
        pp.listnested(c_util)
        print(f"8. {pr.SUMMARY_HUB_OPTION}")
        print(f"0. {pr.EXIT}")
        print()

        while True:
            choice2_str = pp.pinput(pr.ENTER_ACC_NUMBER)
            choice2 = h.validate_numberinput(choice2_str, len(c_util) + 1, allow_zero=True)
            if choice2 is not None:
                break

        if choice2 == 0:
            return None

        if choice2 == len(c_util) + 1:
            summary_hub(save, engine)
            continue

        result_res = calc_loop(choice2, save, engine)
        if not result_res.ok:
            return None
        result = result_res.data
        print(f"\n{result}\n")
        result_list.append(result)

        again = h.ask_yes_no(f"{pr.REDO_CALC_PROMPT} {pr.YN}")
        if not again:
            return


def calc_loop(choice, save, engine):
    return engine.run_calc(choice, save)
