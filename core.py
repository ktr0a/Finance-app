# What todo with data. Calculations, etc.

def testin():
    transactions = [
    {
        "name": "Salary November",
        "category": "income",
        "type": "I",
        "amount": 1450.00,
    },
    {
        "name": "YouTube AdSense",
        "category": "income",
        "type": "I",
        "amount": 320.50,
    },
    {
        "name": "Groceries Lidl",
        "category": "food",
        "type": "E",
        "amount": 42.30,
    },
    {
        "name": "McDonalds",
        "category": "food",
        "type": "E",
        "amount": 11.99,
    },
    {
        "name": "DM Shampoo",
        "category": "selfcare",
        "type": "E",
        "amount": 6.45,
    },
    {
        "name": "Train Ticket",
        "category": "transport",
        "type": "E",
        "amount": 3.00,
    },
    {
        "name": "Netflix Subscription",
        "category": "subscriptions",
        "type": "E",
        "amount": 12.99,
    },
    {
        "name": "Protein Powder",
        "category": "health",
        "type": "E",
        "amount": 24.99,
    },
]
    return(transactions)

def initvars():
    transactions = [] # totallist
    item = {} # one item
    definers = ( # parameters of one item
("name", str), 
("category", str), 
("type", str), 
("amount", float)
)
    for i in range(len(definers)): item[definers[i][0]] = definers[i][1]
    count = 0 # amount of items, used for logic
    return(transactions, definers, item, count)


def sep_ie(transactions):
    income = []
    expense = []
    for i in range(len(transactions)):
        if transactions[i]["type"] == "I":
            income.append(transactions[i])
        elif transactions[i]["type"] == "E":
            expense.append(transactions[i])
        else:
            print(f"invalid type in: {transactions[i]["name"]}; type: {transactions[i]["type"]}") # needs adjustment
    return(income, expense)

def toti(income):
    toti = 0.0
    for i in range(len(income)):
        toti += income[i]["amount"]
    return(toti)

def tote(expense):
    tote = 0.0
    for i in range(len(expense)):
        tote += expense[i]["amount"]
    return(tote)

if __name__ == "__main__":
    """lstdict = testin()
    income, expense = sep_ie(lstdict)
    print(f"Income: {income}\nExpense: {expense}\n")
    print("\n")
    print(toti(income))
    print(tote(expense))"""
    print(initvars()[2])