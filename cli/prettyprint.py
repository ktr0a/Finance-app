import core.config as config
import core.storage as s
import os
import platform
import cli.prompts as pr
import core.config as config


def clearterminal():
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")

def highlight(prompt):
    length = 0
    var = ""
    if isinstance(prompt, list) == True:
        for i in prompt:
            length += len(i)
            var += f"{i}, "
    else: 
        length = len(str(prompt))
        var = str(prompt)
    dashcount = length*"-" + "------"
    print(dashcount)
    print(f"---{var}---")
    print(dashcount)
    return

def listoptions(lst):
    for idx, opt in enumerate(lst, start=1):
        print(f"{idx}. {opt.capitalize()}")

def listdict(dct):
    for key, value in dct.items():
        print(f"  {key.capitalize():<10}: {value}")

def listnested(lst):
    for idx, (name, obj, *args) in enumerate(lst, start=1):
        print(f"{idx}. {name.capitalize()}")

def listnesteddict(lst):
    for idx, item in enumerate(lst, start=1):
        print(f"Item {idx}:")
        for key, value in item.items():
            print(f"  {str(key).capitalize():<10}: {value}")
        print()

def pinput(prompt):
    return(input(f"{prompt} \n").strip())
    