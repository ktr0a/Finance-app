"""Hub responsible for summary generation and display."""
import calendar

import core.config as config

from core.calc_utils import format
from core.sum_utils import SUMMARY_TEMPLATE as sumtemp
from core.sum_utils import sum_util_func as sum_util

import cli.helper as h
import cli.prettyprint as pp
import cli.prompts as pr


def summary_hub(save):
    _, definers, _, _ = config.initvars()

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
                choice2_raw = pp.pinput(f"Enter value for {filterby_key}: ")
                choice2 = h.validate_entry(filterby_key, choice2_raw)
                if choice2 is not None:
                    filterby_value = choice2
                    break

        elif choice == 7:
            filterby_key = definers[4][0]

            while True:
                month_raw = pp.pinput("Enter month (1-12): ").strip()
                if month_raw.isdigit():
                    month = int(month_raw)
                    if 1 <= month <= 12:
                        break
                pp.highlight("Invalid month. Please enter a number between 1 and 12.")

            while True:
                year_raw = pp.pinput("Enter year (YYYY): ").strip()
                if year_raw.isdigit() and len(year_raw) == 4:
                    year = int(year_raw)
                    break
                pp.highlight("Invalid year. Please enter a four-digit year (e.g., 2025).")

            _, last_day = calendar.monthrange(year, month)
            start_date = f"01.{month:02d}.{year}"
            end_date = f"{last_day:02d}.{month:02d}.{year}"
            filterby_value = (start_date, end_date)

        elif choice == 8:
            filterby_key = definers[4][0]

            while True:
                start_raw = pp.pinput("Enter start date (DD.MM.YYYY): ")
                start_date = h.validate_entry("date", start_raw)
                if start_date is not None:
                    break

            while True:
                end_raw = pp.pinput("Enter end date (DD.MM.YYYY): ")
                end_date = h.validate_entry("date", end_raw)
                if end_date is not None:
                    break

            filterby_value = (start_date, end_date)

        else:
            raise SystemExit("summary_hub: invalid choice")

        _, func = sum_util[choice - 1]
        result = func(filterby_key, filterby_value, save)
        transactions_found = result.get("Transactions Analyzed", 0)

        if transactions_found == 0:
            selection = result.get("Key Value Pair", "selection")
            print()
            print(pr.SUMMARY_NO_DATA.format(selection=selection))
            if h.ask_yes_no(f"{pr.SUMMARY_RETRY_PROMPT} {pr.YN}"):
                continue
            return None

        display_summary(result)

        print()
        if h.ask_yes_no(f"{pr.REDO_SORT_PROMPT} {pr.YN}"):
            continue
        break

    return None


def display_summary(result):
    pp.clearterminal()

    if result.keys() == sumtemp.keys():
        print()
        title = result.get("Key Value Pair", "Summary")
        pp.highlight(str(title).capitalize())
        print()

        transactions = result.get("Transactions Analyzed", 0)
        print(f"Transactions analyzed: {format(transactions, 'int')}")
        print()

        for key in ("Total Income", "Total Expense", "Net Balance"):
            value = result.get(key, 0)
            formatted_value = format(value, "money")
            if key == "Total Expense" and not formatted_value.startswith("-"):
                formatted_value = f"-{formatted_value}"
            print(f"{key}: {formatted_value}")

    elif "Special1" in result:
        pp.highlight(result["Special1"])
        print()
        print(f"Transactions analyzed: {format(result['Transactions Analyzed'], 'int')}")
        print()

        categories = result.get("Categories", [])
        totals_formatted = [format(cat["total"], "money") for cat in categories]
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
            cat_count = format(cat["count"], "int")
            print(f"{cat_name.ljust(hi_categoryname).capitalize()}{' ' * spacerh1}{divider1}{cat_count.center(len(H2) - 1)} {divider1}{' ' *spacerh3}{total_str.rjust(hi_type)}")

        print()
        net_balance = format(result.get("Net Balance", 0), "money")
        padding = max(total_length - len("Net Balance: "), 0)
        print(f"Net Balance: {net_balance.rjust(padding)}")

    elif "Special2" in result:
        pp.highlight(result["Special2"])
        print()
        print(f"Transactions analyzed: {format(result.get('Transactions Analyzed', 0), 'int')}")
        print()

        for section in (pr.INCOME, pr.EXPENSE):
            section_data = result.get(section)
            if not isinstance(section_data, dict):
                continue

            print(f"{section}:")
            count_value = section_data.get("count", 0)
            total_value = section_data.get("total", 0)
            print(f"{' ' * pr.spacer3}Count: {format(count_value, 'int')}")
            print(f"{' ' * pr.spacer3}Total: {format(total_value, 'money')}")
            print()

        print(f"Net Balance: {format(result.get('Net Balance', 0), 'money')}")

    else:
        pass
