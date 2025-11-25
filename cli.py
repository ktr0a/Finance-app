# Take userinput & give it to storage.py (& utils.py, if applicable).

import parameters
import time
from calc_utils import calc_util_func as c_util
from sort_utils import sort_util_func as s_util
import storage as s


# main cli 
def start():
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
            error("Please enter a number.")
            continue
        choice = int(choice)
        if 1 <= choice <= len(options):
            break
        else:
            error("Invalid choice. Try again.")
    return choice
def prehub(choice): 
    if choice == 1: # Load existing save
        print("\nloading save...")

        try: save = s.load()
        except Exception:  # Save file exists but is unreadable / corrupted
            print("Save file is corrupted or unreadable.")
            if ask_yes_no("Would you like to create a new save instead? (y/n)"):
                return cr_new_save
            else: exit("o1hub: usr N1")

        if not save:  # no save / empty save
            print("No save detected.")
            if ask_yes_no("Would you like to create a new save instead? (y/n)"):
                return cr_new_save
            else: exit("o1hub: usr N2")
        
        return save
        
    elif choice == 2: # Create save
        return cr_new_save()
    else: exit("prehub: invalid initial choice")
def cr_save(): 
    transactions, definers, _, count = parameters.initvars()

    print("\nHere are the following definers:\n")
    for idx, (name, dtype) in enumerate(definers, start=1):
        print(f"{idx}. {name.capitalize():<10} (type: {dtype.__name__})")
    print("\nPut in your values in the order of the list above.\n")

    if not ask_yes_no("Ready? (y/n)"):
        exit("User cancelled")

    while True:
        item, count = itemloop(definers, count)
        transactions.append(item)

        print("\nSuccessfully added item:\n")
        for key, value in item.items():
            print(f"  {key.capitalize():<10}: {value}")
        print()

        if not ask_yes_no("Do you want add another item? (y/n)"):
            break

    return transactions

def hub(save): # General Hub
    print("Save loaded\n")
    while True:
        choice = input("Would you like to:\n1. Analyze / Calculate\n2. View save\n3. Exit\nEnter the according number: ").strip()
        if not choice.isdigit():
            error("Please enter a number")
            continue
        choice = int(choice)
        if choice not in (1, 2, 3):
            error("Please enter a valid number")
            continue
        elif choice == 1: # Analyze
            new_save = analyze_hub(save)
            if new_save == []:
                continue
            calc_hub(new_save)
        elif choice == 2: # View save
            view_data(save)
        else: exit("hub: User exited choice") # Exit
def analyze_hub(save):
    _, definers, _, _ = parameters.initvars()
    while True:
        print("\nHow do you want to select transactions?\n")
        choice_str = input("1. Analyze all transactions\n" \
        "2. Filter transactions before analyzing\n" \
        "3. Back to main menu\n")
        choice = validate_numberinput(choice_str, 3)
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
            choice = validate_numberinput(choice_str, len(definers))
            if choice is not None:
                filterby_key = definers[choice - 1][0] # Name, category, type or amount
                break

        while True: # filtervalue
            choice_str = input("\nWhat value would you like to filter it by?\n")
            choice = validate_entry(filterby_key, choice_str)
            if choice is not None:
                filterby_value = choice
                break
        
        print(f"\nFiltering by → {filterby_key.capitalize()}: {filterby_value}")

        _, func = s_util[0]
        filtered_save = func(filterby_key, filterby_value, save)

        # if filter = 0
        if not filtered_save and ask_yes_no(f"""\nYour selection "{filterby_key}: {filterby_value}" was not found.\nWould you like to try again? (y/n)""") == True:
            continue

        prettyprint_dict(filtered_save)
        if ask_yes_no(f"\nWould you like to analyze this dataset? (y/n)") == True:
            break
        
        if ask_yes_no(f"\nDo you want to try filtering again? (y/n)") == True:
            continue
        return []
    return filtered_save

def calc_hub(save):
    while True:
        print("\nWhat would you like to calculate?")
        for idx, (label, func) in enumerate(c_util, start=1):
            print(f"{idx}. {label}")
        
        while True:
            choice2_str = input("Enter the according number: ").strip()
            choice2 = validate_numberinput(choice2_str, len(c_util))
            if choice2 is not None:   # valid
                break                 # exit input loop
        
        print(calc_loop(choice2, save)) 

        again = ask_yes_no("Would you like to calculate something else? (y/n)")
        if not again:
            return
        
def view_data(save): # universal view list (hub & analyze hub)
    for idx, entry in enumerate(save, start=1):
        print(f"Item {idx}:")
        for key, value in entry.items():
            print(f"  {key}: {value}")
        print()  # empty line after each dict
    return 

# helpers

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
def ask_yes_no(prompt) -> bool:
    while True:
        choice = input(f"{prompt}\n").upper().strip()
        if choice in ("Y", "YES"):
            return True
        elif choice in ("N", "NO"):
            return False
        else:
            error("Please enter y/n.")
def calc_loop(choice, save): # actual calculation from calc_utils
    label, func = c_util[choice-1]
    result = func(save)
    return(f"{label}: {result}")  
def validate_numberinput(choice_str, max_index):
    if not choice_str.isdigit():
        error("Please enter a number")
        return None

    num = int(choice_str)

    if not (1 <= num <= max_index):
        error("Invalid choice. Try again.")
        return None

    return num
def validate_entry(key, raw_input):
    _, definers, _, _ = parameters.initvars()
    raw = raw_input.strip()
    
    var = [t for dkey, t in definers if dkey == key]

    if not var:
        print(f"ERROR: Unknown field '{key}'.")
        return None

    dtype = var[0]

    if key == "category":
        raw = raw.lower()

    if key == "type":
        raw = raw.upper()
        if raw not in ("I", "E"):
            print("ERROR: Type must be I or E.")
            return None
        return raw

    # Special case: AMOUNT
    if key == "amount":
        raw = raw.replace("-", " ")
        raw = raw.replace(",", ".")

    # General datatype conversion
    try:
        value = dtype(raw)
    except ValueError:
        print(f"ERROR: Expected {dtype.__name__}.")
        return None

    return value
def prettyprint_dict(lst):
    for idx, item in enumerate(lst, start=1):
        print(f"Item {idx}:")
        for key, value in item.items():
            print(f"  {key.capitalize():<10}: {value}")
        print()
def cr_new_save():
    print("\ncreating save...")
    save = cr_save()
    s.save(save)
    print("save created, loading save...")
    return save



# ---Testing---

if __name__ == "__main__":
    save = parameters.testin()
    analyze_hub(save)