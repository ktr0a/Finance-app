# Prompts. Adjust how you like. 

### cli.py
# general

ENTER_ACC_NUMBER = "Enter the according number: "
YN = "(y/n)"
EXIT = "Exit"
INPUT_ANY = "Input any character to continue"
WOULDYOU_PROMPT = "Would you like to:"
WOULDYOU_PROCEED_PROMPT = "Would you like to proceed?"

# start()

PROGRAM_ON = "Program On"
START_OPTIONS = (
    "Load existing save",
    "Create new save",
)

# prehub()
PREHUB_NAME = "Pre-Hub"
LOADING_SAVE = "Loading save..."
FILE_CORRUPTED = "Save file is corrupted or unreadable."
NO_SAVE_DETECTED = "No save was detected"

CR_NEW_SAVE_INSTEAD = "Would you like to create a new save instead?"

# cr_new_save()
CR_SAVE = "Creating save..."
LD_SAVE = "Save created, loading save...."

# cr_save_loop()
CR_SAVE_NAME = "Creating save"
CR_SAVE_LOOP_PROMPT = "Input your Data in the following order:"


SUCCESSFULLY_ADDED = "Successfully added item:"
ADD_ANOTHER_PROMPT = "Would you like to add another item?"

# hub()
HUB_NAME = "General Hub"
SAVE_LOADED = "Save loaded"
HUB_OPTIONS = (
    "Analyze save",
    "View save",
    "Edit save"
)

# analyze_hub()
AHUB_NAME = "Analyzing Hub"
AHUB_PROMPT = "How do you want to select transactions?"
AHUB_OPTIONS = (
    "Analyze all transactions",
    "Filter transactions before analyzing",
)

# filter_save()
FILTER_NAME = "Filtering save"
FILTER_PROMPT_KEY = "What would you like to filter your data by?"
FILTER_PROMPT_VALUE = "What value would you like to filter your data by?"

SELECTION_NOT_FOUND = 'Your selection "{key}: {value}" was not found.'
RETRY_PROMPT = "would you like to try again?"

USE_FILTERED_DATASET = "Would you like to analyze this dataset?"

RETRY_FILTER = "Do you want to try filtering again?"

# calc_hub()
CALC_HUB_NAME = "Calculating Hub"
CALC_HUB_PROMPT = "What would you like to calculate?"
REDO_CALC_PROMPT = "Would you like to calculate something else?"

# edit_hub()
EDIT_HUB_NAME = "Editing Hub"
EDIT_HUB_PROMPT = "What would you like to edit?"
EDIT_HUB_OPTIONS = (
    "Edit a transaction",
    "Delete a transaction",
    "Add a new transaction",
    "View save", # DO NOT DELETE
)

ADD_TRANSACTION_PROMPT = "Add Item Hub"

# edit_transaction()
EDIT_TRANSACTION_PROMPT = "Which Item would you like to edit?"
SEL_ITEM_PROMPT = "What would you like to edit?"
NEW_VALUE_PROMPT = "Enter new value"
REDO_EDIT_TRANSACTION_PROMPT = "Would you like to edit a different value of the item?"
ADD_ITEM_TO_SAVE = "Would you like to save your edits?"

# delete_transactio()
DEL_TRANSACTION_PROMPT = "Which Item would you like to delete?"
RETRY_DEL_PROMPT = "Would you like to try again?"
DEL_ANOTHER_PROMPT = "Would you like to delete another item?"


