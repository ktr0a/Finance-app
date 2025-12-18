"""Hub responsible for summary generation and display."""
import calendar

import core.core_config as core_config

from config.calc_summary import (
    SUMMARY_DISPLAY_KEYS,
    SUMMARY_KEY_MAP,
    NUMBER_OF_TRANSACTIONS_LABEL,
    TRANSACTIONS_ANALYZED_KEY,
    KEY_VALUE_PAIR_LABEL,
)

import cli.helper as h
import cli.prettyprint as pp
import cli.prompts as pr


def summary_hub(save, engine):
    _, definers, _, _ = core_config.initvars()
    menu_res = engine.summary_menu()
    sum_util = menu_res.data if menu_res.ok else []
    template_res = engine.summary_template()
    sumtemp = template_res.data if template_res.ok else {}

    while True:
        pp.clearterminal()
        pp.highlight(pr.SUMMARY_NAME)
        print()
        print(pr.SUMMARY_PROMPT)
        print()
        pp.listnested(sum_util)
        print(f"0. {pr.EXIT}")
        print()

        while True:
            choice_str = pp.pinput(pr.ENTER_ACC_NUMBER)
            choice = h.validate_numberinput(choice_str, len(pr.SUMMARY_OPTIONS), allow_zero=True)
            if choice is not None:
                break

        if choice == 0:
            return None

        if choice in (1, 2, 3):
            filterby_key, filterby_value = None, None

        elif choice in (4, 5, 6):
            filterby_key = definers[choice - 4][0]
            while True:
                print()
                choice2_raw = pp.pinput(pr.ENTER_VALUE_FOR_LABEL.format(field=filterby_key))
                choice2 = h.validate_entry(filterby_key, choice2_raw)
                if choice2 is not None:
                    filterby_value = choice2
                    break

        elif choice == 7:
            filterby_key = definers[4][0]

            while True:
                month_raw = pp.pinput(pr.ENTER_MONTH_PROMPT).strip()
                if month_raw.isdigit():
                    month = int(month_raw)
                    if 1 <= month <= 12:
                        break
                pp.highlight(pr.INVALID_MONTH_MESSAGE)

            while True:
                year_raw = pp.pinput(pr.ENTER_YEAR_PROMPT).strip()
                if year_raw.isdigit() and len(year_raw) == 4:
                    year = int(year_raw)
                    break
                pp.highlight(pr.INVALID_YEAR_MESSAGE)

            _, last_day = calendar.monthrange(year, month)
            start_date = f"01.{month:02d}.{year}"
            end_date = f"{last_day:02d}.{month:02d}.{year}"
            filterby_value = (start_date, end_date)

        elif choice == 8:
            filterby_key = definers[4][0]

            while True:
                start_raw = pp.pinput(pr.ENTER_START_DATE_PROMPT)
                start_date = h.validate_entry("date", start_raw)
                if start_date is not None:
                    break

            while True:
                end_raw = pp.pinput(pr.ENTER_END_DATE_PROMPT)
                end_date = h.validate_entry("date", end_raw)
                if end_date is not None:
                    break

            filterby_value = (start_date, end_date)

        else:
            raise SystemExit(pr.SUMMARY_HUB_INVALID_CHOICE)

        summary_res = engine.summary(
            filterby_key,
            filterby_value,
            save,
            index=choice - 1,
        )
        if not summary_res.ok or not isinstance(summary_res.data, dict):
            raise SystemExit(pr.SUMMARY_HUB_INVALID_CHOICE)
        result = summary_res.data
        transactions_key = SUMMARY_KEY_MAP.get(NUMBER_OF_TRANSACTIONS_LABEL, TRANSACTIONS_ANALYZED_KEY)
        transactions_found = result.get(transactions_key, 0)

        if transactions_found == 0:
            selection = result.get(KEY_VALUE_PAIR_LABEL, pr.SUMMARY_SELECTION_FALLBACK)
            print()
            print(pr.SUMMARY_NO_DATA.format(selection=selection))
            if h.ask_yes_no(f"{pr.SUMMARY_RETRY_PROMPT} {pr.YN}"):
                continue
            return None

        display_summary(result, sumtemp, engine)

        print()
        if h.ask_yes_no(f"{pr.REDO_SORT_PROMPT} {pr.YN}"):
            continue
        break

    return None


def display_summary(result, sumtemp, engine):
    pp.clearterminal()
    transactions_key = SUMMARY_KEY_MAP.get(NUMBER_OF_TRANSACTIONS_LABEL, TRANSACTIONS_ANALYZED_KEY)
    net_balance_label = SUMMARY_DISPLAY_KEYS[-1]

    if result.keys() == sumtemp.keys():
        print()
        title = result.get(KEY_VALUE_PAIR_LABEL, pr.SUMMARY_FALLBACK_TITLE)
        pp.highlight(str(title).capitalize())
        print()

        transactions = result.get(transactions_key, 0)
        print(f"{pr.TRANSACTIONS_ANALYZED_LABEL}: {engine.format_value(transactions, 'int').data}")
        print()

        for key in SUMMARY_DISPLAY_KEYS:
            value = result.get(key, 0)
            formatted_value = engine.format_value(value, "money").data
            if key == "Total Expense" and not formatted_value.startswith("-"):
                formatted_value = f"-{formatted_value}"
            print(f"{key}: {formatted_value}")

    elif "Special1" in result:
        pp.highlight(result["Special1"])
        print()
        print(f"{pr.TRANSACTIONS_ANALYZED_LABEL}: {engine.format_value(result.get(transactions_key, 0), 'int').data}")
        print()

        categories = result.get("Categories", [])
        totals_formatted = [engine.format_value(cat["total"], "money").data for cat in categories]
        hi_categoryname = max((len(str(cat["category_name"])) for cat in categories), default=len(pr.SPECIAL_H1))
        hi_type = len(max(totals_formatted, key=len)) if totals_formatted else len(pr.SPECIAL_H3)

        H1, H2, H3 = pr.SPECIAL_H1, pr.SPECIAL_H2, pr.SPECIAL_H3
        spacerh1 = pr.spacer1
        spacerh3 = pr.spacer2

        divider1 = pr.vertical_divider
        divider2 = pr.horizontal_divider

        total_length = hi_categoryname + spacerh1 + len(H2) + 2 * len(divider1) + hi_type + spacerh3

        print(f"{H1.ljust(hi_categoryname)}{' ' * spacerh1}{divider1}{H2}{divider1}{' ' *spacerh3}{H3.rjust(hi_type)}")

        print(divider2 * total_length)

        for cat, total_str in zip(categories, totals_formatted):
            cat_name = str(cat["category_name"])
            cat_count = engine.format_value(cat["count"], "int").data
            print(f"{cat_name.ljust(hi_categoryname).capitalize()}{' ' * spacerh1}{divider1}{cat_count.center(len(H2) - 1)} {divider1}{' ' *spacerh3}{total_str.rjust(hi_type)}")

        print()
        net_balance = engine.format_value(result.get(net_balance_label, 0), "money").data
        padding = max(total_length - len(f"{net_balance_label}: "), 0)
        print(f"{net_balance_label}: {net_balance.rjust(padding)}")

    elif "Special2" in result:
        pp.highlight(result["Special2"])
        print()
        print(f"{pr.TRANSACTIONS_ANALYZED_LABEL}: {engine.format_value(result.get(transactions_key, 0), 'int').data}")
        print()

        count_label = pr.SPECIAL_H2
        total_label = pr.SPECIAL_H3

        for section in (pr.INCOME, pr.EXPENSE):
            section_data = result.get(section)
            if not isinstance(section_data, dict):
                continue

            print(f"{section}:")
            count_value = section_data.get("count", 0)
            total_value = section_data.get("total", 0)
            print(f"{' ' * pr.spacer3}{count_label}: {engine.format_value(count_value, 'int').data}")
            print(f"{' ' * pr.spacer3}{total_label}: {engine.format_value(total_value, 'money').data}")
            print()

        print(f"{net_balance_label}: {engine.format_value(result.get(net_balance_label, 0), 'money').data}")

    else:
        pass
