# Defined basic data. Basis of other parts.

def testin():
    transactions = [
        # --- Income ---
        {
            "name": "Salary January",
            "category": "income",
            "type": "I",
            "amount": 1450.00,
        },
        {
            "name": "Salary February",
            "category": "income",
            "type": "I",
            "amount": 1450.00,
        },
        {
            "name": "Salary March",
            "category": "income",
            "type": "I",
            "amount": 1450.00,
        },
        {
            "name": "Salary April",
            "category": "income",
            "type": "I",
            "amount": 1450.00,
        },
        {
            "name": "Salary May",
            "category": "income",
            "type": "I",
            "amount": 1450.00,
        },
        {
            "name": "Salary June",
            "category": "income",
            "type": "I",
            "amount": 1450.00,
        },
        {
            "name": "Salary July",
            "category": "income",
            "type": "I",
            "amount": 1450.00,
        },
        {
            "name": "Salary August",
            "category": "income",
            "type": "I",
            "amount": 1450.00,
        },
        {
            "name": "Salary September",
            "category": "income",
            "type": "I",
            "amount": 1450.00,
        },
        {
            "name": "Salary October",
            "category": "income",
            "type": "I",
            "amount": 1450.00,
        },
        {
            "name": "Salary November",
            "category": "income",
            "type": "I",
            "amount": 1450.00,
        },
        {
            "name": "Salary December",
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
            "name": "YouTube AdSense",
            "category": "income",
            "type": "I",
            "amount": 287.15,
        },
        {
            "name": "YouTube AdSense",
            "category": "income",
            "type": "I",
            "amount": 410.75,
        },
        {
            "name": "Sponsorship Deal",
            "category": "income",
            "type": "I",
            "amount": 600.00,
        },
        {
            "name": "Freelance Editing",
            "category": "income",
            "type": "I",
            "amount": 120.00,
        },
        {
            "name": "Freelance Editing",
            "category": "income",
            "type": "I",
            "amount": 95.50,
        },
        {
            "name": "Gift from Parents",
            "category": "income",
            "type": "I",
            "amount": 50.00,
        },
        {
            "name": "Refund Amazon",
            "category": "income",
            "type": "I",
            "amount": 25.99,
        },

        # --- Food ---
        {
            "name": "McDonalds",
            "category": "food",
            "type": "E",
            "amount": 11.99,
        },
        {
            "name": "McDonalds",
            "category": "food",
            "type": "E",
            "amount": 8.49,
        },
        {
            "name": "McDonalds",
            "category": "food",
            "type": "E",
            "amount": 9.99,
        },
        {
            "name": "Groceries Lidl",
            "category": "food",
            "type": "E",
            "amount": 42.30,
        },
        {
            "name": "Groceries Lidl",
            "category": "food",
            "type": "E",
            "amount": 15.80,
        },
        {
            "name": "Groceries Lidl",
            "category": "food",
            "type": "E",
            "amount": 33.40,
        },
        {
            "name": "Billa Groceries",
            "category": "food",
            "type": "E",
            "amount": 23.50,
        },
        {
            "name": "Billa Groceries",
            "category": "food",
            "type": "E",
            "amount": 19.75,
        },
        {
            "name": "Kebab Shop",
            "category": "food",
            "type": "E",
            "amount": 7.50,
        },
        {
            "name": "Kebab Shop",
            "category": "food",
            "type": "E",
            "amount": 8.00,
        },
        {
            "name": "Bakery Snack",
            "category": "food",
            "type": "E",
            "amount": 3.20,
        },
        {
            "name": "Bakery Snack",
            "category": "food",
            "type": "E",
            "amount": 4.10,
        },

        # --- Health ---
        {
            "name": "Protein Powder",
            "category": "health",
            "type": "E",
            "amount": 24.99,
        },
        {
            "name": "Protein Powder",
            "category": "health",
            "type": "E",
            "amount": 24.99,
        },
        {
            "name": "Protein Powder",
            "category": "health",
            "type": "E",
            "amount": 29.99,
        },
        {
            "name": "Gym Membership",
            "category": "health",
            "type": "E",
            "amount": 29.99,
        },
        {
            "name": "Gym Membership",
            "category": "health",
            "type": "E",
            "amount": 29.99,
        },
        {
            "name": "Creatine",
            "category": "health",
            "type": "E",
            "amount": 14.50,
        },
        {
            "name": "Multivitamins",
            "category": "health",
            "type": "E",
            "amount": 9.99,
        },
        {
            "name": "Doctor Visit",
            "category": "health",
            "type": "E",
            "amount": 35.00,
        },
        {
            "name": "Pharmacy Medicine",
            "category": "health",
            "type": "E",
            "amount": 12.75,
        },

        # --- Transport ---
        {
            "name": "Train Ticket",
            "category": "transport",
            "type": "E",
            "amount": 3.00,
        },
        {
            "name": "Train Ticket",
            "category": "transport",
            "type": "E",
            "amount": 3.00,
        },
        {
            "name": "Train Ticket",
            "category": "transport",
            "type": "E",
            "amount": 3.00,
        },
        {
            "name": "Monthly Pass",
            "category": "transport",
            "type": "E",
            "amount": 49.00,
        },
        {
            "name": "Uber Ride",
            "category": "transport",
            "type": "E",
            "amount": 12.50,
        },
        {
            "name": "Uber Ride",
            "category": "transport",
            "type": "E",
            "amount": 9.75,
        },
        {
            "name": "Taxi Ride",
            "category": "transport",
            "type": "E",
            "amount": 18.00,
        },
        {
            "name": "Scooter Rental",
            "category": "transport",
            "type": "E",
            "amount": 4.20,
        },
        {
            "name": "Scooter Rental",
            "category": "transport",
            "type": "E",
            "amount": 6.10,
        },

        # --- Subscriptions ---
        {
            "name": "Netflix Subscription",
            "category": "subscriptions",
            "type": "E",
            "amount": 12.99,
        },
        {
            "name": "Netflix Subscription",
            "category": "subscriptions",
            "type": "E",
            "amount": 12.99,
        },
        {
            "name": "Spotify Subscription",
            "category": "subscriptions",
            "type": "E",
            "amount": 9.99,
        },
        {
            "name": "Spotify Subscription",
            "category": "subscriptions",
            "type": "E",
            "amount": 9.99,
        },
        {
            "name": "YouTube Premium",
            "category": "subscriptions",
            "type": "E",
            "amount": 11.99,
        },
        {
            "name": "iCloud Storage",
            "category": "subscriptions",
            "type": "E",
            "amount": 0.99,
        },
        {
            "name": "Domain qluo.dev",
            "category": "subscriptions",
            "type": "E",
            "amount": 12.00,
        },
        {
            "name": "Adobe Subscription",
            "category": "subscriptions",
            "type": "E",
            "amount": 24.99,
        },

        # --- Self-care ---
        {
            "name": "DM Shampoo",
            "category": "selfcare",
            "type": "E",
            "amount": 6.45,
        },
        {
            "name": "DM Shampoo",
            "category": "selfcare",
            "type": "E",
            "amount": 6.45,
        },
        {
            "name": "Face Wash",
            "category": "selfcare",
            "type": "E",
            "amount": 5.99,
        },
        {
            "name": "Moisturizer",
            "category": "selfcare",
            "type": "E",
            "amount": 7.49,
        },
        {
            "name": "Toothpaste Colgate",
            "category": "selfcare",
            "type": "E",
            "amount": 2.89,
        },
        {
            "name": "Toothbrush",
            "category": "selfcare",
            "type": "E",
            "amount": 3.49,
        },
        {
            "name": "Haircut",
            "category": "selfcare",
            "type": "E",
            "amount": 18.00,
        },
        {
            "name": "Barber Tip",
            "category": "selfcare",
            "type": "E",
            "amount": 2.00,
        },

        # --- Entertainment ---
        {
            "name": "Cinema Ticket",
            "category": "entertainment",
            "type": "E",
            "amount": 10.50,
        },
        {
            "name": "Cinema Ticket",
            "category": "entertainment",
            "type": "E",
            "amount": 10.50,
        },
        {
            "name": "Cinema Snack Combo",
            "category": "entertainment",
            "type": "E",
            "amount": 7.99,
        },
        {
            "name": "PC Game Steam",
            "category": "entertainment",
            "type": "E",
            "amount": 19.99,
        },
        {
            "name": "PC Game Steam",
            "category": "entertainment",
            "type": "E",
            "amount": 39.99,
        },
        {
            "name": "Robux Purchase",
            "category": "entertainment",
            "type": "E",
            "amount": 9.99,
        },
        {
            "name": "Robux Purchase",
            "category": "entertainment",
            "type": "E",
            "amount": 19.99,
        },
        {
            "name": "Concert Ticket",
            "category": "entertainment",
            "type": "E",
            "amount": 45.00,
        },

        # --- Education / Projects ---
        {
            "name": "Udemy Course",
            "category": "education",
            "type": "E",
            "amount": 12.99,
        },
        {
            "name": "Udemy Course",
            "category": "education",
            "type": "E",
            "amount": 9.99,
        },
        {
            "name": "Programming Book",
            "category": "education",
            "type": "E",
            "amount": 29.99,
        },
        {
            "name": "Electronics Components",
            "category": "education",
            "type": "E",
            "amount": 17.50,
        },
        {
            "name": "Arduino Kit",
            "category": "education",
            "type": "E",
            "amount": 35.00,
        },
        {
            "name": "Raspberry Pi",
            "category": "education",
            "type": "E",
            "amount": 55.00,
        },
        {
            "name": "3D Printer Filament",
            "category": "education",
            "type": "E",
            "amount": 22.00,
        },
        {
            "name": "3D Printer Filament",
            "category": "education",
            "type": "E",
            "amount": 22.00,
        },

        # --- Housing / Home ---
        {
            "name": "Rent",
            "category": "housing",
            "type": "E",
            "amount": 550.00,
        },
        {
            "name": "Electricity Bill",
            "category": "housing",
            "type": "E",
            "amount": 42.30,
        },
        {
            "name": "Internet Bill",
            "category": "housing",
            "type": "E",
            "amount": 24.90,
        },
        {
            "name": "Water Bill",
            "category": "housing",
            "type": "E",
            "amount": 15.20,
        },
        {
            "name": "Cleaning Supplies",
            "category": "housing",
            "type": "E",
            "amount": 8.75,
        },
        {
            "name": "Laundry Coins",
            "category": "housing",
            "type": "E",
            "amount": 4.00,
        },
        {
            "name": "Desk Lamp",
            "category": "housing",
            "type": "E",
            "amount": 19.99,
        },
        {
            "name": "Office Chair",
            "category": "housing",
            "type": "E",
            "amount": 89.99,
        },

        # --- Other / Misc ---
        {
            "name": "Gift for Friend",
            "category": "other",
            "type": "E",
            "amount": 15.00,
        },
        {
            "name": "Gift for Friend",
            "category": "other",
            "type": "E",
            "amount": 20.00,
        },
        {
            "name": "Charity Donation",
            "category": "other",
            "type": "E",
            "amount": 10.00,
        },
        {
            "name": "Bank Fee",
            "category": "other",
            "type": "E",
            "amount": 1.99,
        },
        {
            "name": "ATM Withdrawal Fee",
            "category": "other",
            "type": "E",
            "amount": 2.50,
        },
        {
            "name": "Phone Case",
            "category": "other",
            "type": "E",
            "amount": 9.99,
        },
        {
            "name": "USB-C Cable",
            "category": "other",
            "type": "E",
            "amount": 6.99,
        },
        {
            "name": "Power Bank",
            "category": "other",
            "type": "E",
            "amount": 24.99,
        },
        {
            "name": "Screen Protector",
            "category": "other",
            "type": "E",
            "amount": 4.99,
        },
        {
            "name": "Notebook",
            "category": "other",
            "type": "E",
            "amount": 2.50,
        },
        {
            "name": "Pens Pack",
            "category": "other",
            "type": "E",
            "amount": 3.20,
        },
    ]

    return transactions

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