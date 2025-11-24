# take cli.py and save to json. take json and turn into output for util.py

import json
import os
from pathlib import Path

DATA_FILE = Path("save.json")

def save(lst):
    with DATA_FILE.open("w", encoding="utf-8") as f:
        json.dump(lst, f, indent=4)

def load():
    if DATA_FILE.exists() == False:
        return False # no save yet
    else:
        with DATA_FILE.open("r", encoding="utf-8") as f:
            return json.load(f) # returns list of dicts
        
def delsavereq():
    if DATA_FILE.exists() == False:
        return False # no save 
    else:
        os.remove("save.json")
        return True # successful

# ---Testing---

if __name__ == "__main__":
    """from parameters import testin
    lst = testin()
    savelst(lst)
    print("1")
    print(delsavereq())"""