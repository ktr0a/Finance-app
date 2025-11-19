# What todo with data. Calculations, etc.

def testin():
    transactions = [
    {
        "name": "Salary November",
        "category": "income",
        "type": "income",
        "amount": 1450.00,
    },
    {
        "name": "YouTube AdSense",
        "category": "income",
        "type": "income",
        "amount": 320.50,
    },
    {
        "name": "Groceries Lidl",
        "category": "food",
        "type": "expense",
        "amount": 42.30,
    },
    {
        "name": "McDonalds",
        "category": "food",
        "type": "expense",
        "amount": 11.99,
    },
    {
        "name": "DM Shampoo",
        "category": "selfcare",
        "type": "expense",
        "amount": 6.45,
    },
    {
        "name": "Train Ticket",
        "category": "transport",
        "type": "expense",
        "amount": 3.00,
    },
    {
        "name": "Netflix Subscription",
        "category": "subscriptions",
        "type": "expense",
        "amount": 12.99,
    },
    {
        "name": "Protein Powder",
        "category": "health",
        "type": "expense",
        "amount": 24.99,
    },
]
    return(transactions)

def sep_ie(transactions):
    income = {}
    expense = {}
    for i in transactions:
        if transactions[i]["type"] == "income":
            income += transactions[i]
        elif transactions[i]["type"] == "expense":
            expense += transactions[i]
        else:
            print(f"invalid type in: {transactions[i]["name"]}; type: {transactions[i]["type"]}")
    return(income, expense)

lstdict = testin()
print(sep_ie(lstdict))