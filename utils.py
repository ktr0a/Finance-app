# Calculations with list of items & parameters (dicts). Returns 

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
    if income == []:
        print("Run sep_ie() first; income[] empty")
        return()
    toti = 0.0
    for i in range(len(income)):
        toti += income[i]["amount"]
    return(toti)

def tote(expense):
    if expense == []:
        print("Run sep_ie() first; expense[] empty")
        return()
    tote = 0.0
    for i in range(len(expense)):
        tote += expense[i]["amount"]
    return(tote)


