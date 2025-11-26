import core.config as config
import core.storage as s


def prettyprint_dict(lst):
    for idx, item in enumerate(lst, start=1):
        print(f"Item {idx}:")
        for key, value in item.items():
            print(f"  {key.capitalize():<10}: {value}")
        print()

def view_data(save): # universal view list (hub & analyze hub)
    for idx, entry in enumerate(save, start=1):
        print(f"Item {idx}:")
        for key, value in entry.items():
            print(f"  {key}: {value}")
        print()  # empty line after each dict
    return 

def highlight(prompt):
    length = len(prompt)
    dashcount = length*"-" + "------"
    print(dashcount)
    print(f"---{prompt}---")
    print(dashcount)
    return
