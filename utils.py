# Calculations with list of items & parameters (dicts). Returns 

def sep_ie(transactions): # predecessor to toti & tote
    income = []
    expense = []
    for i in range(len(transactions)):
        if transactions[i]["type"] == "I":
            income.append(transactions[i])
        elif transactions[i]["type"] == "E":
            expense.append(transactions[i])
        else:
            print(f"invalid type in: {transactions[i]["name"]}; type: {transactions[i]["type"]}") # needs adjustment
    return income, expense

def toti(save):
    income, _ = sep_ie(save)
    return sum(t["amount"] for t in income)

def tote(save):
    _, expense = sep_ie(save)
    return sum(t["amount"] for t in expense)

# UTILS - imported by main.py

util_func = [
    ("Total income", toti),
    ("Total expense", tote),
]
