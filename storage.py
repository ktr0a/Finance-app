# take cli.py and save to json. take json and turn into output for core.py

import json
import os
from pathlib import Path

DATA_FILE = Path("save.json")

def savelst(lst):
    with DATA_FILE.open("w", encoding="utf-8") as f:
        json.dump(lst, f, indent=4)

def loadlst():
    if DATA_FILE.exists() == False:
        return(False) # no save yet
    else:
        with DATA_FILE.open("r", encoding="utf-8") as f:
            return json.load(f) # returns list of dicts
        
def delsavereq():
    if DATA_FILE.exists() == False:
        return(False) # no save 
    else:
        os.remove("save.json")
        return(True) # successful


if __name__ == "__main__":
    from core import testin
    lst = testin()
    savelst(lst)
    print("1")
    print(delsavereq())