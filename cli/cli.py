# Take userinput & give it to storage.py (& utils.py, if applicable).

import core.config as config

from core.calc_utils import calc_util_func as c_util
from core.sort_utils import sort_util_func as s_util

import core.storage as s

import cli.helper as h
import cli.prettyprint as pp

import cli.prompts as pr

import time




# main cli 
def start(): # Ask if Load or Create Save?
    pp.clearterminal()
    print(pr.PROGRAM_ON)
    print()
    print(pr.WOULDYOU_PROMPT)
    print()
    pp.listoptions(pr.START_OPTIONS)
    print(pr.EXIT)
    print()

    while True:
        choice_str = pp.pinput(pr.ENTER_ACC_NUMBER)
        choice = h.validate_numberinput(choice_str, len(pr.START_OPTIONS) + 1)
        if choice is not None:   # valid
            break                 # exit input loop
    return choice

def prehub(choice): # Load or Create Save
    pp.clearterminal()
    pp.highlight(pr.PREHUB)
    if choice == 1: # Load existing save
        print(pr.LOADING_SAVE)

        try: save = s.load()
        except Exception:  # Save file exists but is unreadable / corrupted
            print(pr.FILE_CORRUPTED)
            if h.ask_yes_no(f"{pr.CR_NEW_SAVE_INSTEAD} {pr.YN}"):
                return cr_new_save()
            else: exit("o1hub: usr N1")

        if not save:  # no save / empty save
            print(pr.NO_SAVE_DETECTED)
            if h.ask_yes_no(f"{pr.CR_NEW_SAVE_INSTEAD} {pr.YN}"):
                return cr_new_save()
            else: exit("o1hub: usr N2")
        
        return save
        
    elif choice == 2: # Create save
        return cr_new_save()
    else: exit("prehub: invalid initial choice")

def hub(save): # General Hub
    print(pr.SAVE_LOADED)
    time.sleep(1)
    while True:

        pp.clearterminal()
        pp.highlight("HUB")
        print()
        print(pr.WOULDYOU_PROMPT)
        print()
        pp.listoptions(pr.HUB_OPTIONS)
        print(pr.EXIT)
        print()

        while True:
            choice_str = pp.pinput(pr.ENTER_ACC_NUMBER)
            choice = h.validate_numberinput(choice_str, len(pr.HUB_OPTIONS) + 1)
            if choice is not None:   # valid
                break                 # exit input loop

        if choice == 1: # Analyze
            new_save = analyze_hub(save)
            if new_save == []:
                continue
            calc_hub(new_save)
        elif choice == 2: # View save
            pp.view_data(save)
            pp.pinput(pr.INPUT_ANY)
        else: 
            pp.clearterminal()
            exit("hub: User exited choice") # Exit

def analyze_hub(save): # Filterting Hub
    pp.clearterminal()
    _, definers, _, _ = config.initvars()

    print()
    print(pr.AHUB_PROMPT)
    print()
    pp.listoptions(pr.AHUB_OPTIONS)
    print(pr.EXIT)
    print()

    while True:
        choice_str = pp.pinput(pr.ENTER_ACC_NUMBER)
        choice = h.validate_numberinput(choice_str, len(pr.AHUB_OPTIONS) + 1)
        if choice is not None: break
    
    if choice == 1:
        return save
    elif choice == 2:
        return analyze_filtered_save(save, definers)
    else: exit()

def analyze_filtered_save(save, definers):
    if save == []:
        print("shits empty")
        return []
    while True:        
        pp.clearterminal()

        _, definers, _, _ = config.initvars()

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
        print(f"Filtering by -> {filterby_key}")
        
        while True: # filtervalue
            choice_str = pp.pinput(pr.FILTER_PROMPT_VALUE)
            choice = h.validate_entry(filterby_key, choice_str)
            if choice is not None:
                filterby_value = choice
                break

        pp.clearterminal()
        print(f"\nFiltering by -> {filterby_key.capitalize()}: {filterby_value}")

        _, func = s_util[0]
        filtered_save = func(filterby_key, filterby_value, save)

        # if filter = 0
        print(pr.SELECTION_NOT_FOUND.format(key=filterby_key, value=filterby_value))
        if not filtered_save and h.ask_yes_no(f"{pr.RETRY_PROMPT} {pr.YN}"):
            continue

        pp.prettyprint_dict(filtered_save)
        if h.ask_yes_no(f"{pr.USE_FILTERED_DATASET} {pr.YN}") == True:
            break
        
        if h.ask_yes_no(f"{pr.RETRY_FILTER} {pr.YN}") == True:
            continue
        return []
    return filtered_save

def calc_hub(save): # Calculating Hub
    result_list = []
    while True:
        pp.clearterminal()

        if result_list != []:
            pp.highlight(result_list)
        
        print()
        print(pr.CALC_HUB_PROMPT)
        print()
        pp.listnested(c_util)
        print()
        
        while True:
            choice2_str = pp.pinput(pr.ENTER_ACC_NUMBER)
            choice2 = h.validate_numberinput(choice2_str, len(c_util))
            if choice2 is not None:   # valid
                break                 # exit input loop
        
        result = calc_loop(choice2, save)
        print(f"\n{result}\n")
        result_list.append(result)

        again = h.ask_yes_no(f"{pr.REDO_CALC_PROMPT} {pr.YN}")
        if not again:
            return

def cr_save_loop(): # Generate Save 
    transactions, definers, _, count = config.initvars()

    pp.clearterminal()
    print()
    print(pr.CR_SAVE_LOOP_PROMPT)
    print()
    pp.listnested(definers)
    print()

    if not h.ask_yes_no(f"{pr.WOULDYOU_PROCEED_PROMPT} {pr.YN}"):
        exit("User cancelled")

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
            raw = pp.pinput(f"{name.capitalize()}, {dtype.__name__}: ")

            # use shared validator
            value = h.validate_entry(name, raw)
            if value is None:
                # validation failed → ask again
                continue

            item[name] = value
            break

    count += 1
    return item, count
def calc_loop(choice, save): # Calculate
    label, func = c_util[choice-1]
    result = func(save)
    return(f"{label}: {result}")  

def cr_new_save():
    print()
    print(f"{pr.CR_SAVE}")
    save = cr_save_loop()
    s.save(save)
    print()
    print(f"{pr.LD_SAVE}")
    return save




# ---Testing---

if __name__ == "__main__":
    save = config.testin()
    analyze_hub(save)