# Calculations with list of items & parameters (dicts). Returns 

def format(value, mode: str) -> str:
    if mode == "money":
        return f"{value:.2f}€"
    elif mode == "int":
        return str(value)
    
    else: return str(value) # failsafe

def split_IE(transactions): # seperate i/e
    income = []
    expense = []
    for i in range(len(transactions)):
        if transactions[i]["type"] == "I":
            income.append(transactions[i])
        elif transactions[i]["type"] == "E":
            expense.append(transactions[i])
        else: 
            raise ValueError(f"Invalid type in: {transactions[i]['name']}; type: {transactions[i]['type']}")
    return income, expense

def toti_raw(save) -> float:
    income, _ = split_IE(save)
    return sum(t["amount"] for t in income)

def tote_raw(save) -> float:
    _, expense = split_IE(save)
    return sum(t["amount"] for t in expense)

def netbal_raw(save) -> float:
    return toti_raw(save) - tote_raw(save)

def count_transactions(save) -> int:
    return len(save)

def avg_transaction_amount(save) -> float:
    if not save:
        return 0.0
    return sum(v["amount"] for v in save) / len(save)

def max_transaction_amount(save) -> float:
    if not save:
        return 0.0
    return max(v["amount"] for v in save)

def min_transaction_amount(save) -> float:
    if not save:
        return 0.0
    return min(v["amount"] for v in save)

# UTILS - imported by cli/cli.py

calc_util_func = [
    ("Total Income", toti_raw, "money"),
    ("Total Expense", tote_raw, "money"),
    ("Net Balance", netbal_raw, "money"),
    ("Number of Transactions", count_transactions, "int"),
    ("Average transaction amount", avg_transaction_amount, "money"),
    ("Max transaction amount", max_transaction_amount, "money"),
    ("Min transaction amount", min_transaction_amount, "money"),

]
