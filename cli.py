# Take userinput & give it to storage (& analysis, if applicable).
#         "name": "Salary November",
#        "category": "income",
#        "type": "I",
#        "amount": 1450.00,
import core

def stop(): # check if stop after each item
    usr_i = input("Do you want to stop? (y/n)\n").upper()
    if usr_i in ("Y", "YES", "YE"):
        return(True)
    elif usr_i in ("N", "NO"):
        return
 
def itemloop(): # loop for filling item dict
    global count, definers, item
    print("\n")
    if True == True: # irrelevant. If statement to collapse in IDE
        suffix = ["st", "nd", "rd", "th"]
        if count < 3:
            print(f"{count+1}{suffix[count]} Item:")
        else:
            print(f"{count+1}{suffix[3]} Item:")
    #
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
            except:
                print(f"ERROR: Expected {dtype.__name__}.")
                continue
                    
            item[name] = value
            break
    print(f"\nItem {count+1}:\n{item}\n")
    count += 1
    return(item)

def main(): # main loop
    core.initvars()
    print("\n")
    print(f"""Here are the following definers: {definers}\nPut in your values in the order of the list above.\n\nThis means:""")
    var = 1 
    for name, dtype in definers:
        print(f"""{var}. "{name.capitalize()}" in the format "{dtype}" """)
        var += 1
    print("Ready? y/n")
    usr_i = input().strip().upper()
    #
    if usr_i in ("Y", "YES", "YE"):
        while True:
            if count == 0: pass
            elif stop() == True: break
            transactions.append(itemloop().copy())
            print("successfully added")
            for i in range(len(definers)): item.pop(definers[i][0]) # clears item{}

    elif usr_i in ("N", "NO"):
        exit("User cancelled")
    
    return(transactions)
    

if __name__ == "__main__":
    transactions, definers, item, count = core.initvars()
    print(main())
