# Prompts. Adjust how you like. 

### cli.py
# general

ENTER_ACC_NUMBER = "Enter the corresponding number: "
YN = "(y/n)"
EXIT = "Exit"
INPUT_ANY = "Press any character to continue"
WOULDYOU_PROMPT = "What would you like to do?"
WOULDYOU_PROCEED_PROMPT = "Would you like to proceed?"
WOULDYOU_INSTEAD_PROMPT = "Would you like to instead: "

# start()

START = "Starting Hub"
PROGRAM_ON = "Program On"
START_OPTIONS = (
    "Load existing save",
    "Restore from latest backup",
    "Create new save",
)

# prehub()
PREHUB_NAME = "Pre-hub"
LOADING_SAVE = "Loading save..."
FILE_CORRUPTED = "Save file is corrupted or unreadable."
NO_SAVE_DETECTED = "No save was detected"

CONFIRM_BACKUP_OVERRIDE = "This will override storage/save.json with the latest backup."
NO_BACKUPS_FOUND = "No backups found to restore"
BACKUP_FAILED = "Failed to restore backup"
BACKUP_REINSTATED = "Backup successfully reinstated as save"

CR_NEW_SAVE_INSTEAD = "Would you like to create a new save instead?"

# cr_new_save()
CR_SAVE = "Creating save..."
LD_SAVE = "Save created, loading save..."

# cr_save_loop()
CR_SAVE_NAME = "Create transactions"
CR_SAVE_LOOP_PROMPT = "Enter your data in the following order:"

SUCCESSFULLY_ADDED = "Successfully added transaction:"
ADD_ANOTHER_PROMPT = "Would you like to add another transaction?"


# hub()
HUB_NAME = "Main hub"
SAVE_LOADED = "Save loaded."
HUB_OPTIONS = (
    "Analyze save",
    "View save",
    "Edit save",
    "Create backup now",
    "Restore from previous backups",
    "Undo/Redo"
)

# analyze_hub()
AHUB_NAME = "Analysis hub"
AHUB_PROMPT = "How do you want to select transactions?"
AHUB_OPTIONS = (
    "Analyze all transactions",
    "Filter transactions before analyzing",
)

# filter_save()
FILTER_NAME = "Filter transactions"
FILTER_PROMPT_KEY = "Which field would you like to filter by?"
FILTER_PROMPT_VALUE = "Enter the value to filter by:"

SELECTION_NOT_FOUND = 'Your selection "{key}: {value}" was not found.'
RETRY_PROMPT = "Would you like to try again?"

USE_FILTERED_DATASET = "Would you like to analyze only this filtered dataset?"

RETRY_FILTER = "Would you like to try a different filter?"

# calc_hub()
CALC_HUB_NAME = "Calculation Hub"
CALC_HUB_PROMPT = "What would you like to calculate?"
REDO_CALC_PROMPT = "Would you like to calculate something else?"

# summary_hub()
SUMMARY_NAME = "Summary Hub"
SUMMARY_PROMPT = "How would you like to summarize?"
SUMMARY_OPTIONS = (
    "All-time summary",
    "General Category overview", # category
    "General Income vs Expense overview", # I/E
    "Summary by Name", # Name
    "Summary by category", # category
    "Summary by type (income vs expense)", # I/E
    "Summary by month", # time
    "Summary by custom date range", # time
)
REDO_SORT_PROMPT = "Would you like to summarize something else?"
SUMMARY_NO_DATA = 'No transactions were found for "{selection}".'
SUMMARY_RETRY_PROMPT = "Would you like to try a different summary?"

# display_summary()
DISPLAY_SUMMARY_PROMPT = "Press any character to return to the Summary hub."
SPECIAL_H1, SPECIAL_H2, SPECIAL_H3 = "Category", "Count", "Total"
spacer1 = 5
spacer2 = 4
vertical_divider = " | "
horizontal_divider = "-"

INCOME = "Income"
EXPENSE = "Expense"
spacer3 = 6


# edit_hub()
EDIT_HUB_NAME = "Edit hub"
EDIT_HUB_OPTIONS = (
    "Edit a transaction",
    "Delete a transaction",
    "Add a new transaction",
    "View save",  # DO NOT DELETE
)

SUMMARY_HUB_OPTION = "Summary hub"

ADD_TRANSACTION_PROMPT = "Add transaction"

# edit_transaction()
EDIT_TRANSACTION_PROMPT = "Which transaction would you like to edit?"
SEL_ITEM_PROMPT = "Which field would you like to edit?"
NEW_VALUE_PROMPT = "Enter the new value:"
REDO_EDIT_TRANSACTION_PROMPT = "Would you like to edit another field in this transaction?"
ADD_ITEM_TO_SAVE = "Save these changes?"

# del_transaction()
DEL_TRANSACTION_PROMPT = "Which transaction would you like to delete?"
RETRY_DEL_PROMPT = "Would you like to select a different transaction?"
DEL_ANOTHER_PROMPT = "Would you like to delete another transaction?"

# undoredo_hub()
UNDOREDO_HUB_NAME = "Undo / Redo Menu"
UNDOREDO_HUB_OPTIONS = (
    "Undo last action",
    "Redo last action",
    "View current save",
)
