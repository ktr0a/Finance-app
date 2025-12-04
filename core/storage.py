# take cli.py and save to json. take json and turn into output for util.py

import json
import os
import shutil

from pathlib import Path
from datetime import datetime as dt
import core.config as config


MAIN_DATA_FILE = Path("save.json")

BACKUP_DIR = "backups/"
BACKUP_DATA_FILE_NAME = "save_backup_"

DEFAULT_DATE = "01.01.2001"

def save(lst, *args): # save list: None, True
    try:
        with MAIN_DATA_FILE.open("w", encoding="utf-8") as f:
            json.dump(lst, f, indent=4)
    except (OSError, TypeError, ValueError): return None # failsafe
    return True

def load(): # Load save: None/False/True, None/data/data
    if MAIN_DATA_FILE.exists() == False:
        return None, None  # no save yet

    try:
        with MAIN_DATA_FILE.open("r", encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, json.JSONDecodeError, TypeError, ValueError):
        return None, None

    if not isinstance(data, list):
        return None, None

    for txn in data:
        if isinstance(txn, dict) and "date" not in txn:
            txn["date"] = DEFAULT_DATE

    if not data:
        return False, data

    return True, data  # returns status flag plus list of dicts

def cr_backup_json(): # Back up the current save from save json: False, True
    if not MAIN_DATA_FILE.exists():
        return False  # nothing to back up

    time_now = dt.now().strftime("%Y%m%d_%H%M%S_%f")
    backup_file = Path(f"{BACKUP_DIR}{BACKUP_DATA_FILE_NAME}{time_now}.json")
    backup_file.parent.mkdir(parents=True, exist_ok=True)

    # Copy the existing save.json as-is
    shutil.copy2(MAIN_DATA_FILE, backup_file)

    # Prune old backups
    del_backup()

    return True

def cr_backup_lst(lst): #  Back up the current save with passed list: None, True
    time_now = dt.now().strftime("%Y%m%d_%H%M%S_%f")
    backup_file = Path(f"{BACKUP_DIR}{BACKUP_DATA_FILE_NAME}{time_now}.json")

    backup_file.parent.mkdir(parents=True, exist_ok=True)

    try:
        with backup_file.open("w", encoding="utf-8") as f:
            json.dump(lst, f, indent=4)

        del_backup()

    except (OSError, TypeError, ValueError):
        return None
    return True

def edit_and_backup_save(lst, *args):
    
    cr_backup_json()
    return save(lst, *args)

def del_save(): # Delete Main save: False, None, True
    if not MAIN_DATA_FILE.exists():
        return False
    try:
        MAIN_DATA_FILE.unlink()
    except OSError:
        return None
    return True

def restore_latest_backup(): # Restore backup based on creation time: None, False, True
    backups = _sort_backups(ascending=False)  # newest -> oldest

    if not backups:
        return None  # nothing to restore

    newest = backups[0]

    restore_status = restore_backup_file(newest)
    if restore_status is None:
        return None  # unreadable or failed to load backup
    if restore_status is False:
        return False  # failed to write main save

    try:
        newest.unlink()
    except OSError:
        return False

    return True


def restore_backup():
    return restore_latest_backup()

def del_backup(): # Delete backup based on creation time: None, True
    backups = _sort_backups(ascending=True)  # oldest -> newest

    if not backups:
        return None  # no backup folder or no backups

    backup_deleted = False

    while len(backups) > config.AMOUNT_OF_BACKUPS:
        oldest = backups.pop(0)  # oldest is always at index 0
        oldest.unlink()
        backup_deleted = True

    return backup_deleted

def _sort_backups(ascending: bool): # Sort backup
    # return list of backup path obj, by modified time
    # ascending = True, False (oldest, newest)

    backup_dir = Path(BACKUP_DIR)

    if not backup_dir. exists():
        return [] # no backup folder
    
    backups = list(backup_dir.glob(f"{BACKUP_DATA_FILE_NAME}*.json"))

    file_time_pairs = []

    for file in backups:
        mtime = file.stat().st_mtime
        file_time_pairs.append((file, mtime))

    file_time_pairs.sort(key=lambda pair: pair[1])

    if ascending == True:
        return [file for file, _ in file_time_pairs]

    else:
        file_time_pairs.reverse()
        return [file for file, _ in file_time_pairs]
        
def list_backups() -> list[Path]:
    return _sort_backups(ascending=False)

def restore_backup_file(path: Path) -> bool | None:
    try:
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, json.JSONDecodeError, TypeError, ValueError):
        return None  # unreadable

    # If you already switched save() to atomic, this is safe:
    return True if save(data) is True else False


    


# ---Testing---

if __name__ == "__main__":
    """from parameters import testin
    lst = testin()
    savelst(lst)
    print("1")
    print(delsavereq())"""
