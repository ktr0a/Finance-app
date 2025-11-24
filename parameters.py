# Defined basic data. Basis of other parts.

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
("type", str),              # Used in cli.py: DO NOT CHANGE NAME
("amount", float)
)
    for i in range(len(definers)): item[definers[i][0]] = definers[i][1]
    count = 0 # amount of items, used for logic
    return(transactions, definers, item, count)

# ---Testing---

if __name__ == "__main__":
    """lstdict = testin()
    income, expense = sep_ie(lstdict)
    print(f"Income: {income}\nExpense: {expense}\n")
    print("\n")
    print(toti(income))
    print(tote(expense
    print(initvars()[2])"""