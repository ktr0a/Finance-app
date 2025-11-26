# Take userinput & give it to storage.py (& utils.py, if applicable).

import core.config as config

from core.calc_utils import calc_util_func as c_util
from core.sort_utils import sort_util_func as s_util

import core.storage as s

import cli.helper as h
import cli.prettyprint as pp
import time




# main cli 
def start(): # Ask if Load or Create Save?
    print("\nProgram On\n")

    options = [ # put into parameters
        "Load existing save",
        "Create new save"
    ]

    while True:
        print("Would you like to:")
        for idx, opt in enumerate(options, start=1):
            print(f"{idx}. {opt}")

        choice = input("Enter the according number: ").strip()
        if not choice.isdigit(): # digit validator
            h.error("Please enter a number.")
            continue
        choice = int(choice)
        if 1 <= choice <= len(options):
            break
        else:
            h.error("Invalid choice. Try again.")
    return choice

def prehub(choice): # Load or Create Save
    if choice == 1: # Load existing save
        print("\nloading save...")

        try: save = s.load()
        except Exception:  # Save file exists but is unreadable / corrupted
            print("Save file is corrupted or unreadable.")
            if h.ask_yes_no("Would you like to create a new save instead? (y/n)"):
                return cr_new_save()
            else: exit("o1hub: usr N1")

        if not save:  # no save / empty save
            print("No save detected.")
            if h.ask_yes_no("Would you like to create a new save instead? (y/n)"):
                return cr_new_save()
            else: exit("o1hub: usr N2")
        
        return save
        
    elif choice == 2: # Create save
        return cr_new_save()
    else: exit("prehub: invalid initial choice")

def hub(save): # General Hub
    print("Save loaded\n")
    while True:
        choice = input("Would you like to:\n1. Analyze / Calculate\n2. View save\n3. Exit\nEnter the according number: ").strip()
        if not choice.isdigit():
            h.error("Please enter a number")
            continue
        choice = int(choice)
        if choice not in (1, 2, 3):
            h.error("Please enter a valid number")
            continue
        elif choice == 1: # Analyze
            new_save = analyze_hub(save)
            if new_save == []:
                continue
            calc_hub(new_save)
        elif choice == 2: # View save
            pp.view_data(save)
        else: exit("hub: User exited choice") # Exit

def analyze_hub(save): # Filterting Hub
    _, definers, _, _ = config.initvars()
    while True:
        print("\nHow do you want to select transactions?\n")
        choice_str = input("1. Analyze all transactions\n" \
        "2. Filter transactions before analyzing\n" \
        "3. Back to main menu\n")
        choice = h.validate_numberinput(choice_str, 3)
        if choice == 1:
            return save
        elif choice == 2:
            break
        else:
            return[]
    while True:        
        print("\nWhat would you like to filter your data by?")
        for idx, (name, dtype) in enumerate(definers, start=1):
            print(f"{idx}. {name.capitalize()}")

        while True: # filterkey
            choice_str = input("Enter the according number: ").strip()
            choice = h.validate_numberinput(choice_str, len(definers))
            if choice is not None:
                filterby_key = definers[choice - 1][0] # Name, category, type or amount
                break

        while True: # filtervalue
            choice_str = input("\nWhat value would you like to filter it by?\n")
            choice = h.validate_entry(filterby_key, choice_str)
            if choice is not None:
                filterby_value = choice
                break
        
        print(f"\nFiltering by → {filterby_key.capitalize()}: {filterby_value}")

        _, func = s_util[0]
        filtered_save = func(filterby_key, filterby_value, save)

        # if filter = 0
        if not filtered_save and h.ask_yes_no(f"""\nYour selection "{filterby_key}: {filterby_value}" was not found.\nWould you like to try again? (y/n)""") == True:
            continue

        pp.prettyprint_dict(filtered_save)
        if h.ask_yes_no(f"\nWould you like to analyze this dataset? (y/n)") == True:
            break
        
        if h.ask_yes_no(f"\nDo you want to try filtering again? (y/n)") == True:
            continue
        return []
    return filtered_save

def calc_hub(save): # Calculating Hub
    while True:
        print("\nWhat would you like to calculate?")
        for idx, (label, func) in enumerate(c_util, start=1):
            print(f"{idx}. {label}")
        
        while True:
            choice2_str = input("Enter the according number: ").strip()
            choice2 = h.validate_numberinput(choice2_str, len(c_util))
            if choice2 is not None:   # valid
                break                 # exit input loop
        
        print(calc_loop(choice2, save)) 

        again = h.ask_yes_no("Would you like to calculate something else? (y/n)")
        if not again:
            return

def cr_save_loop(): # Generate Save 
    transactions, definers, _, count = config.initvars()

    print("\nHere are the following definers:\n")
    for idx, (name, dtype) in enumerate(definers, start=1):
        print(f"{idx}. {name.capitalize():<10} (type: {dtype.__name__})")
    print("\nPut in your values in the order of the list above.\n")

    if not h.ask_yes_no("Ready? (y/n)"):
        exit("User cancelled")

    while True:
        item, count = item_loop(definers, count)
        transactions.append(item)

        print("\nSuccessfully added item:\n")
        for key, value in item.items():
            print(f"  {key.capitalize():<10}: {value}")
        print()

        if not h.ask_yes_no("Do you want add another item? (y/n)"):
            break

    return transactions

def item_loop(definers, count): # Generate each item for Save
    print("\n")
    suffix = ["st", "nd", "rd", "th"]
    if count < 3:
        print(f"{count+1}{suffix[count]} Item:")
    else:
        print(f"{count+1}{suffix[3]} Item:")

    item = {}

    for name, dtype in definers: # Put usr_i in item{}
        while True:
            raw = input(f"{name.capitalize()}, {dtype.__name__}: ").strip()

            if name == "category": # make category all lower
                raw = raw.lower()
            
            if name == "type": # validator for Type: only I/E
                raw = raw.upper()
                if raw not in ("I", "E"):
                    print("ERROR: Type must be I or E.")
                    continue
                item[name] = raw 
                break

            if name == "amount":
                raw = raw.replace("-"," ")
                raw = raw.replace(",",".")
            try: # general datatype validator
                value = dtype(raw) 
            except ValueError:
                print(f"ERROR: Expected {dtype.__name__}.")
                continue
                    
            item[name] = value
            break
    print(f"\nItem {count+1}:\n{item}\n")
    count += 1
    return item, count

def calc_loop(choice, save): # Calculate
    label, func = c_util[choice-1]
    result = func(save)
    return(f"{label}: {result}")  

def cr_new_save():
    print("\ncreating save...")
    save = cr_save_loop()
    s.save(save)
    print("save created, loading save...")
    return save




# ---Testing---

if __name__ == "__main__":
    save = config.testin()
    analyze_hub(save)