# Take userinput & give it to storage.py (& utils.py, if applicable).
import calendar
import copy

import core.config as config

from core.calc_utils import calc_util_func as c_util
from core.calc_utils import format
from core.sort_utils import sort_util_func as s_util
from core.sum_utils import sum_util_func as sum_util

from core.sum_utils import SUMMARY_TEMPLATE as sumtemp

import core.storage as s

import cli.helper as h
import cli.prettyprint as pp

import cli.prompts as pr

import time




# main cli 
def start(): # Ask if Load or Create Save?
    pp.clearterminal()
    pp.highlight(pr.PROGRAM_ON)
    print()
    print(pr.WOULDYOU_PROMPT)
    print()
    pp.listoptions(pr.START_OPTIONS)
    print(f"0. {pr.EXIT}")
    print()

    while True:
        choice_str = pp.pinput(pr.ENTER_ACC_NUMBER)
        choice = h.validate_numberinput(choice_str, len(pr.START_OPTIONS), allow_zero = True)
        if choice is not None:   # valid
            break                 # exit input loop
    return choice

def prehub(choice): # Load or Create Save
    pp.clearterminal()
    pp.highlight(pr.PREHUB_NAME)

    if choice == 0: # Exit
        return None
    
    elif choice == 1: # Load existing save
        print(pr.LOADING_SAVE)

        try: save = s.load()
        except Exception:  # Save file exists but is unreadable / corrupted
            print(pr.FILE_CORRUPTED)
            if h.ask_yes_no(f"{pr.CR_NEW_SAVE_INSTEAD} {pr.YN}"):
                return cr_new_save()
            else: 
                return None

        if not save:  # no save / empty save
            print(pr.NO_SAVE_DETECTED)
            if h.ask_yes_no(f"{pr.CR_NEW_SAVE_INSTEAD} {pr.YN}"):
                return cr_new_save()
            else: 
                return None
        
        return save
        
    elif choice == 2: # Create save
        save = cr_new_save()
        if save is None:
            return None
        return save
    
    else: exit("prehub: invalid initial choice")

def cr_new_save():
    print()
    print(f"{pr.CR_SAVE}")
    save = cr_save_loop(pr.CR_SAVE_NAME)
    if save is None:
        return None
    s.save(save)
    print()
    print(f"{pr.LD_SAVE}")
    return save
def cr_save_loop(PROMPT): # Generate Save 
    transactions, definers, _, count = config.initvars()

    pp.clearterminal()
    pp.highlight(PROMPT)
    print()
    print(pr.CR_SAVE_LOOP_PROMPT)
    print()
    pp.listnested(definers)
    print()

    if not h.ask_yes_no(f"{pr.WOULDYOU_PROCEED_PROMPT} {pr.YN}"):
        return None

    while True:
        item, count = item_loop(definers, count)
        transactions.append(item)

        print()
        print(pr.SUCCESSFULLY_ADDED)
        for key, value in item.items():
            print(f"  {key.capitalize():<10}: {value}")
        print()

        if not h.ask_yes_no(f"{pr.ADD_ANOTHER_PROMPT} {pr.YN}"):
            break

    return transactions
def item_loop(definers, count): # Generate each item for Save
    pp.clearterminal()
    suffix = ["st", "nd", "rd", "th"]
    if count < 3:
        print(f"{count+1}{suffix[count]} Item:")
    else:
        print(f"{count+1}{suffix[3]} Item:")

    item = {}

    for name, dtype in definers: # Put usr_i in item{}
        while True:
            prompt_label = f"{name.capitalize()}, {dtype.__name__}"
            if name == "date":
                prompt_label = f"{name.capitalize()} (DD.MM.YYYY), {dtype.__name__}"

            raw = pp.pinput(f"{prompt_label}: ")

            # use shared validator
            value = h.validate_entry(name, raw)
            if value is None:
                # validation failed -> ask again
                continue

            item[name] = value
            break

    count += 1
    return item, count



def hub(save): # General Hub
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
            choice = h.validate_numberinput(choice_str, len(pr.HUB_OPTIONS), allow_zero = True)
            if choice is not None:   # valid
                break                 # exit input loop
        
        if choice == 0: # Exit
            return None
        
        elif choice == 1: # Analyze
            new_save = analyze_hub(save)
            if new_save is None: # 
                continue
            calc_hub(new_save)

        elif choice == 2: # View save
            pp.listnesteddict(save)
            pp.pinput(pr.INPUT_ANY)

        elif choice == 3:  # Edit save
            edited_save = edit_hub(save)
            if edited_save is not None:
                save = edited_save          # use updated data
                s.save(save)                # persist it


        else: # Failsafe/debug
            print("ERROR: Invaoic choice, hub")
            return None # Exit


def analyze_hub(save): # Filterting Hub
    _, definers, _, _ = config.initvars()

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
        choice = h.validate_numberinput(choice_str, len(pr.AHUB_OPTIONS), allow_zero = True)
        if choice is not None: break
    
    if choice == 0: # Exit
        return None

    elif choice == 1:
        return save
    
    elif choice == 2:
        return filter_save(save, definers)
    
    else: # Failsafe/debug
        print("ERROR: Invaoic choice, ahub")
        return None
def filter_save(save, definers):
    if not save: # no/empty save
        print("save is empty")
        return None
    
    while True:        
        _, definers, _, _ = config.initvars()

        pp.clearterminal()
        pp.highlight(pr.FILTER_NAME)
        print()
        print(pr.FILTER_PROMPT_KEY)
        print()
        pp.listnested(definers)
        print()

        while True: # filterkey
            choice_str = pp.pinput(pr.ENTER_ACC_NUMBER)
            choice = h.validate_numberinput(choice_str, len(definers))
            if choice is not None:
                filterby_key = definers[choice - 1][0] # Name, category, type or amount
                break

        pp.clearterminal()
        pp.highlight(pr.FILTER_NAME)
        print()
        print(f"Filtering by -> {filterby_key}")
        print()
        
        while True: # filtervalue
            choice_str = pp.pinput(pr.FILTER_PROMPT_VALUE)
            choice = h.validate_entry(filterby_key, choice_str)
            if choice is not None:
                filterby_value = choice
                break

        pp.clearterminal()
        pp.highlight(pr.FILTER_NAME)
        print()
        print(f"\nFiltering by -> {filterby_key.capitalize()}: {filterby_value}")
        print()

        _, func = s_util[0]
        filtered_save = func(filterby_key, filterby_value, save)

        # if filter = 0
        if not filtered_save:
            print(pr.SELECTION_NOT_FOUND.format(key=filterby_key, value=filterby_value))
            if h.ask_yes_no(f"{pr.RETRY_PROMPT} {pr.YN}"):
                continue
            return None

        pp.listnesteddict(filtered_save)
        if h.ask_yes_no(f"{pr.USE_FILTERED_DATASET} {pr.YN}") == True:
            break
        
        if h.ask_yes_no(f"{pr.RETRY_FILTER} {pr.YN}") == True:
            continue

        return None # dont use result + dont retry
    
    return filtered_save # use result


def calc_hub(save): # Calculating Hub
    result_list = [] # to display what has been calculated
    while True:
        pp.clearterminal()
        pp.highlight(pr.CALC_HUB_NAME)

        if result_list != []: # if smth has been calculated
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
            choice2 = h.validate_numberinput(choice2_str, len(c_util) + 1, allow_zero = True)
            if choice2 is not None:   # valid
                break                 # exit input loop

        if choice2 == 0: # Exit
            return None
        
        if choice2 == len(c_util) + 1: # Summarizehub
            summary_hub(save)
            continue

        result = calc_loop(choice2, save)
        print(f"\n{result}\n")
        result_list.append(result)

        again = h.ask_yes_no(f"{pr.REDO_CALC_PROMPT} {pr.YN}")
        if not again:
            return
def calc_loop(choice, save):
    label, func, mode = c_util[choice-1]
    result = func(save)           
    output = format(result, mode)
    if "expense" in label.lower() and not output.startswith("-"):
        output = f"-{output}"

    return f"{label}: {output}"

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

        while True: # choice
            choice_str = pp.pinput(pr.ENTER_ACC_NUMBER)
            choice = h.validate_numberinput(choice_str, len(pr.SUMMARY_OPTIONS), allow_zero = True)
            if choice is not None:   # valid
                break                 # exit input loop
        
        if choice == 0: # Exit
            return None
        
        elif choice in (1, 2, 3): # All-time summary, General overview, Income vs Expense overview
            filterby_key, filterby_value = None, None
        
        elif choice in (4, 5, 6): # Summary by name, category, type
            filterby_key = definers[choice - 4][0]
            while True: # filtervalue
                print()
                choice2_raw = pp.pinput(f"Enter value for {filterby_key}: ")
                choice2 = h.validate_entry(filterby_key, choice2_raw)
                if choice2 is not None:
                    filterby_value = choice2
                    break
            
        elif choice == 7: # Summary by month
            filterby_key = definers[4][0]  # date

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
    
        elif choice == 8: # Summary by custom date range
            filterby_key = definers[4][0]  # date
            # get start date
            while True:
                start_raw = pp.pinput("Enter start date (DD.MM.YYYY): ")
                start_date = h.validate_entry("date", start_raw)
                if start_date is not None:
                    break
            # get end date
            while True:
                end_raw = pp.pinput("Enter end date (DD.MM.YYYY): ")
                end_date = h.validate_entry("date", end_raw)
                if end_date is not None:
                    break
            
            filterby_value = (start_date, end_date)
        
        # Calculate summary
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

        total_length = hi_categoryname  + spacerh1 + len(H2) + 2*len(divider1) + hi_type + spacerh3

        print(f"{H1.ljust(hi_categoryname)}{' ' * spacerh1}{divider1}{H2}{divider1}{' ' *spacerh3}{H3.rjust(hi_type)}") # Titles

        print(divider2 * total_length) # divider

        for cat, total_str in zip(categories, totals_formatted): # each category
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

    else: pass



def edit_hub(save):
    # print
    while True:
        pp.clearterminal()
        _, definers, _, _ = config.initvars()
        pp.highlight(pr.EDIT_HUB_NAME)
        print()
        print(pr.EDIT_HUB_PROMPT)
        print()
        pp.listoptions(pr.EDIT_HUB_OPTIONS)
        print(f"0. {pr.EXIT}")
        print()
        # ask 

        while True:
            choice_str = pp.pinput(pr.ENTER_ACC_NUMBER)
            choice = h.validate_numberinput(choice_str, len(pr.EDIT_HUB_OPTIONS), allow_zero = True)
            if choice is not None:   # valid
                break                 # exit input loop
        
        if choice == 0: # Exit
            return None
        
        elif choice == 1: # Edit transaction
            return edit_transaction(save, definers)
        
        elif choice == 2: # Delete transaction
            return delete_transaction(save)
        
        elif choice == 3: # Add new transaction
            return add_transaction(save)
        
        elif choice == 4: # View save
            pp.listnesteddict(save)
            pp.pinput(pr.INPUT_ANY)
            continue
        
        else: # Failsafe/debug
            print("ERROR: Invaoic choice, hub")
        pass

def edit_transaction(save, definers):
    pp.listnesteddict(save)
    print()
    print(pr.EDIT_TRANSACTION_PROMPT)
    print(f"0. {pr.EXIT}")
    print()

    while True:
        choice_str = pp.pinput(pr.ENTER_ACC_NUMBER)
        choice = h.validate_numberinput(choice_str, len(save), allow_zero = True)
        if choice is not None:   # valid
            break                 # exit input loop

    if choice == 0: # exit
        return None
    
    item_index = choice
    item = copy.deepcopy(save[choice - 1])
    print(f"Selected Item:\nItem: {choice}")

    while True:
        pp.listdict(item)
        print()
        print(pr.SEL_ITEM_PROMPT)
        print()
        pp.listnested(definers)
        print(f"0. {pr.EXIT}")
        print()

        while True: # select key
            choice_str = pp.pinput(pr.ENTER_ACC_NUMBER)
            key_choice = h.validate_numberinput(choice_str, len(definers), allow_zero = True)
            if key_choice is not None:   # valid
                break                 # exit input loop

        if key_choice == 0: # exit
            return None

        selected_key = definers[key_choice - 1][0]
        print(f"Selected key: {selected_key.capitalize()}")
        print()
        
        while True: # edit value
            raw = pp.pinput(f"{pr.NEW_VALUE_PROMPT}: ")
            value = h.validate_entry(selected_key, raw)
            if value is None:
                continue
            break

        item[selected_key] = value # insert new value

        pp.listdict(item)

        if h.ask_yes_no(f"{pr.REDO_EDIT_TRANSACTION_PROMPT} {pr.YN}"):
            continue

        if h.ask_yes_no(f"{pr.ADD_ITEM_TO_SAVE} {pr.YN}"):
            save[item_index - 1] = item
            return save
        
        return None
def delete_transaction(save):
    deleted_any = False

    while True:
        pp.listnesteddict(save)
        print()
        print(pr.DEL_TRANSACTION_PROMPT)
        print(f"0. {pr.EXIT}")
        print()

        while True:
            choice_str = pp.pinput(pr.ENTER_ACC_NUMBER)
            choice = h.validate_numberinput(choice_str, len(save), allow_zero = True)
            if choice is not None:   # valid
                break                 # exit input loop

        if choice == 0:
            return save if deleted_any else None
        
        item = save[choice - 1]
        print(f"Selected Item for deletion (Item {choice}):")
        pp.listdict(item)

        if not h.ask_yes_no(f"{pr.WOULDYOU_PROCEED_PROMPT} {pr.YN}"): # try again?
            if h.ask_yes_no(f"{pr.RETRY_DEL_PROMPT} {pr.YN}"): 
                continue
            return save if deleted_any else None

        # actually delete
        save.pop(choice - 1)
        deleted_any = True

        if not save: # failsafe: save has no more items
            print("No more transactions.")
            return save

        if not h.ask_yes_no(f"{pr.DEL_ANOTHER_PROMPT} {pr.YN}"):
            return save
def add_transaction(save):
    addition = cr_save_loop(pr.ADD_TRANSACTION_PROMPT)
    if addition is None:
        return None

    for i in addition:
        save.append(i)

    return save 

# ---Testing---

if __name__ == "__main__":
    save = config.testin()
    print(summary_hub(save))
