# Calculations with list of items & parameters (dicts). Returns 

def format(amount: float) -> str:
    return f"{amount:.2f}€"

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

def toti_raw(save) -> float:
    income, _ = split_IE(save)
    return sum(t["amount"] for t in income)

def tote_raw(save) -> float:
    _, expense = split_IE(save)
    return sum(t["amount"] for t in expense)

def netbal_raw(save) -> float:
    return toti_raw(save) - tote_raw(save)


# UTILS - imported by main.py

calc_util_func = [
    ("Total income", toti_raw),
    ("Total expense", tote_raw),
    ("Net Balance", netbal_raw),
]
