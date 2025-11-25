# Calculations with list of items & parameters (dicts). Returns 

currency = "€" # future plans - adaptive currency

def split_IE(transactions): # seperate i/e
    income = []
    expense = []
    for i in range(len(transactions)):
        if transactions[i]["type"] == "I":
            income.append(transactions[i])
        elif transactions[i]["type"] == "E":
            expense.append(transactions[i])
        else:
            print(f"""invalid type in: {transactions[i]["name"]}; type: {transactions[i]["type"]}""") 
    return income, expense

def toti(save):
    income, _ = split_IE(save)
    toti = sum(t["amount"] for t in income)
    return str(toti) + currency

def tote(save):
    _, expense = split_IE(save)
    tote = sum(t["amount"] for t in expense)
    return str(tote) + currency

def netbal(save):
    income, expense = split_IE(save)
    netbal = sum(i["amount"] for i in income) - sum(e["amount"] for e in expense)
    return str(netbal) + currency



# UTILS - imported by main.py

calc_util_func = [
    ("Total income", toti),
    ("Total expense", tote),
    ("Net Balance", netbal),
]
