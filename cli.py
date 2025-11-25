# Take userinput & give it to storage.py (& utils.py, if applicable).

import parameters
import time
from utils import util_func as utils
import storage as s

# main cli 
def cr_save(): 
    transactions, definers, _, count = parameters.initvars()
    print("\n")

    print("Here are the following definers:\n")
    for idx, (name, dtype) in enumerate(definers, start=1):
        print(f'{idx}. {name.capitalize():<10} (type: {dtype.__name__})')
    print("\nPut in your values in the order of the list above.\n")

    if not ask_yes_no("Ready? (y/n)"):
        exit("User cancelled")

    while True:
        item, count = itemloop(definers, count)
        transactions.append(item)

        print("\nSuccessfully added item:\n")
        for key, value in item.items():
            print(f"  {key}: {value}")
        print()

        if not ask_yes_no("Do you want add another item? (y/n)"):
            break

    return transactions
def ld_save(choice): 
    while True:
        if choice == 1: # Load existing save
            print("\nloading save...")
            save = s.load()
            if not save: # nosave/nothing in exising save
                print("No save detected")
                while True: 
                    choice2 = ask_yes_no("Would you like to create a new save instead? (y/n)")
                    if choice2:
                        choice = 2
                        break
                    else:
                        exit("o1hub: usr N")
            else: 
                break
        elif choice == 2: # Create save
            print("\ncreating save...")
            save = cr_save()
            s.save(save)
            print("save created, loading save...")
            break
    return save
def selutilfunc(save):
    while True: # Select utils function
        print("\nWhat would you like to calculate?")
        for idx, (label, func) in enumerate(utils, start=1):
            print(f"{idx}. {label}")
        choice2 = input("Enter the according number: ").strip()
        if not choice2.isdigit():
            error("Please enter a number")
            continue
        choice2 = int(choice2)
        if 1 <= choice2 <= len(utils):
            break
        else:
            error("Invalid choice. Try again.")
    label, func = utils[choice2-1]
    result = func(save)
    
    return label, result
def calc_loop(save):
    while True:
        label, result = selutilfunc(save)
        print(f"{label}: {result}")

        again = ask_yes_no("Would you like to calculate something else? (y/n)")
        if not again:
            break
def hub(save):
    print("Save loaded\n")
    while True:
        choice = input("Would you like to:\n1. Calculate\n2. View save\n3. Exit\nEnter the according number: ").strip()
        if not choice.isdigit():
            error("Please enter a number")
            continue
        choice = int(choice)
        if choice not in (1, 2, 3):
            error("Please enter a valid number")
            continue
        elif choice == 1: # Calculate
            calc_loop(save)
        elif choice == 2: # View save
            for idx, entry in enumerate(save, start=1):
                print(f"Item {idx}:")
                for key, value in entry.items():
                    print(f"  {key}: {value}")
                print()  # empty line after each dict
        else: exit("hub: User exited choice") # Exit
def start():
    print("\nProgram On\n")

    options = [
        "Load existing save",
        "Create new save"
    ]

    while True:
        print("Would you like to:")
        for idx, opt in enumerate(options, start=1):
            print(f"{idx}. {opt}")

        choice = input("Enter the according number: ").strip()
        if not choice.isdigit():
            error("Please enter a number.")
            continue
        choice = int(choice)
        if 1 <= choice <= len(options):
            break
        else:
            error("Invalid choice. Try again.")
    return choice

# helpers
def ask_yes_no(prompt) -> bool:
    while True:
        choice = input(f"{prompt}\n").upper().strip()
        if choice in ("Y", "YES"):
            return True
        elif choice in ("N", "NO"):
            return False
        else:
            error("Please enter y/n.")
def error(prompt):
    length = len(prompt)
    dashcount = length*"-" + "------"
    print(dashcount)
    print(f"---{prompt}---")
    print(dashcount)
    return
def itemloop(definers, count): # loop for filling item dict
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

            if name == "type": # validator for Type: only I/E
                raw = raw.upper()
                if raw not in ("I", "E"):
                    print("ERROR: Type must be I or E.")
                    continue
                item[name] = raw 
                break
            elif name == "amount":
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

# ---Testing---

"""if __name__ == "__main__":
    print(main())"""
