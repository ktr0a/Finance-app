# Take userinput & give it to storage.py (& utils.py, if applicable).

import parameters

def stop() -> bool: # check if stop after each item
    while True:
        usr_i = input("Do you want to stop? (y/n)\n").upper().strip()
        if usr_i in ("Y", "YES", "YE"):
            return True
        elif usr_i in ("N", "NO"):
            return False
        else:
            print("Please answer with y/n.")
 
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

def main(): # main loop
    transactions, definers, _, count = parameters.initvars()
    print("\n")
    print(f"""Here are the following definers: {definers}\nPut in your values in the order of the list above.\n\nThis means:""")
    var = 1 
    for name, dtype in definers:
        print(f"""{var}. "{name.capitalize()}" in the format "{dtype.__name__}" """)
        var += 1
    print("Ready? y/n")
    usr_i = input().strip().upper()
    
    if usr_i in ("Y", "YES", "YE"):
        while True:
            item, count = itemloop(definers, count)
            transactions.append(item) # add item to transactions[]
            print("successfully added")

            if stop(): 
                break

    elif usr_i in ("N", "NO"):
        exit("User cancelled")
    
    return transactions
    
# ---Testing---

if __name__ == "__main__":
    print(main())
