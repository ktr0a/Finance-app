from finance_app.core.schema import DATE_EXAMPLE, DATE_FORMAT_HUMAN
from finance_app.cli.ui.params import INT_FORMAT_MODE, MONEY_FORMAT_MODE

# Calculation and summary formatting labels
CALC_CONFIG = [
    ("Total Income", MONEY_FORMAT_MODE),
    ("Total Expense", MONEY_FORMAT_MODE),
    ("Net Balance", MONEY_FORMAT_MODE),
    ("Number of Transactions", INT_FORMAT_MODE),
    ("Average transaction amount", MONEY_FORMAT_MODE),
    ("Max transaction amount", MONEY_FORMAT_MODE),
    ("Min transaction amount", MONEY_FORMAT_MODE),
]

KEY_VALUE_PAIR_LABEL = "Key Value Pair"
TRANSACTIONS_ANALYZED_KEY = "Transactions Analyzed"

TOTAL_INCOME_LABEL = CALC_CONFIG[0][0]
TOTAL_EXPENSE_LABEL = CALC_CONFIG[1][0]
NET_BALANCE_LABEL = CALC_CONFIG[2][0]
NUMBER_OF_TRANSACTIONS_LABEL = CALC_CONFIG[3][0]

REQUIRED_CALCS = (
    NUMBER_OF_TRANSACTIONS_LABEL,
    TOTAL_INCOME_LABEL,
    TOTAL_EXPENSE_LABEL,
    NET_BALANCE_LABEL,
)

SUMMARY_TEMPLATE = {
    KEY_VALUE_PAIR_LABEL: "",
    TRANSACTIONS_ANALYZED_KEY: 0,
    TOTAL_INCOME_LABEL: 0.0,
    TOTAL_EXPENSE_LABEL: 0.0,
    NET_BALANCE_LABEL: 0.0,
}

SUMMARY_KEY_MAP = {
    NUMBER_OF_TRANSACTIONS_LABEL: TRANSACTIONS_ANALYZED_KEY,
    TOTAL_INCOME_LABEL: TOTAL_INCOME_LABEL,
    TOTAL_EXPENSE_LABEL: TOTAL_EXPENSE_LABEL,
    NET_BALANCE_LABEL: NET_BALANCE_LABEL,
}

SUMMARY_DISPLAY_KEYS = (TOTAL_INCOME_LABEL, TOTAL_EXPENSE_LABEL, NET_BALANCE_LABEL)

CATEGORY_OVERVIEW_TITLE = "Category Overview"
INCOME_EXPENSE_OVERVIEW_TITLE = "Income vs Expense"

# General prompts and input helpers
ENTER_ACC_NUMBER = "Enter the corresponding number: "
YN = "(y/n)"
YN_PROMPT = "Please enter y/n."
INPUT_ANY = "Press any character to continue"
EXIT = "Exit"
WOULDYOU_PROMPT = "What would you like to do?"
WOULDYOU_PROCEED_PROMPT = "Would you like to proceed?"
WOULDYOU_INSTEAD_PROMPT = "Would you like to instead: "
ENTER_NUMBER_PROMPT = "Please enter a number"
INVALID_CHOICE = "Invalid choice. Try again."

# Start hub
START = "Starting Hub"
PROGRAM_ON = "Program On"
START_OPTIONS = (
    "Load existing save",
    "Restore from latest backup",
    "Create new save",
)

# Prehub
PREHUB_NAME = "Pre-hub"
LOADING_SAVE = "Loading save..."
FILE_CORRUPTED = "Save file is corrupted or unreadable."
NO_SAVE_DETECTED = "No save was detected"
CONFIRM_BACKUP_OVERRIDE = "This will override storage/save.json with the latest backup."
NO_BACKUPS_FOUND = "No backups found to restore"
BACKUP_FAILED = "Failed to restore backup"
BACKUP_REINSTATED = "Backup successfully reinstated as save"
CR_NEW_SAVE_INSTEAD = "Would you like to create a new save instead?"
UNKNOWN_LOAD_STATE = "Unknown load state"
FAILED_TO_WRITE_SAVE = "Failed to write save file."

# Create new save
CR_SAVE = "Creating save..."
LD_SAVE = "Save created, loading save..."
CR_SAVE_NAME = "Create transactions"
CR_SAVE_LOOP_PROMPT = "Enter your data in the following order:"
SUCCESSFULLY_ADDED = "Successfully added transaction:"
ADD_ANOTHER_PROMPT = "Would you like to add another transaction?"
ITEM_LABEL = "Item"
ITEM_SUFFIXES = ("st", "nd", "rd", "th")

# Main hub
HUB_NAME = "Main hub"
SAVE_LOADED = "Save loaded."
HUB_OPTIONS = (
    "Analyze save",
    "View save",
    "Edit save",
    "Create backup now",
    "Restore from previous backups",
    "Undo/Redo",
)
NO_CHANGES_MADE = "No changes made."
UNDO_BACKUP_FAILED = "Undo Backup failed"
CONTINUE_WITHOUT_UNDO_BACKUP = "Continue without undo backup?"
FAILED_SAVE_CHANGES = "Failed to save changes to disk."
BACKUP_CREATED = "Backup created."
RESTORE_BACKUP_TITLE = "Restore backup"
SELECT_BACKUP_TO_RESTORE = "Select a backup to restore:"
SELECTED_BACKUP_UNREADABLE = "Selected backup is unreadable."
BACKUP_RELOAD_FAILED = "Backup restored but failed to reload save from disk."
WARNING_BACKUP_DELETE = "Warning: Failed to delete one or more backups."

# Analyze hub
AHUB_NAME = "Analysis hub"
AHUB_PROMPT = "How do you want to select transactions?"
AHUB_OPTIONS = (
    "Analyze all transactions",
    "Filter transactions before analyzing",
)
FILTER_NAME = "Filter transactions"
FILTER_PROMPT_KEY = "Which field would you like to filter by?"
FILTER_PROMPT_VALUE = "Enter the value to filter by:"
SELECTION_NOT_FOUND = 'Your selection "{key}: {value}" was not found.'
RETRY_PROMPT = "Would you like to try again?"
USE_FILTERED_DATASET = "Would you like to analyze only this filtered dataset?"
RETRY_FILTER = "Would you like to try a different filter?"
SAVE_IS_EMPTY = "save is empty"
FILTERING_BY_LABEL = "Filtering by -> {field}"
FILTERING_BY_VALUE_LABEL = "Filtering by -> {field}: {value}"
ENTER_VALUE_FOR_LABEL = "Enter value for {field}: "

# Calculation hub
CALC_HUB_NAME = "Calculation Hub"
CALC_HUB_PROMPT = "What would you like to calculate?"
REDO_CALC_PROMPT = "Would you like to calculate something else?"
SUMMARY_HUB_OPTION = "Summary hub"

# Summary hub
SUMMARY_NAME = "Summary Hub"
SUMMARY_PROMPT = "How would you like to summarize?"
SUMMARY_OPTIONS = (
    "All-time summary",
    "General Category overview",
    "General Income vs Expense overview",
    "Summary by Name",
    "Summary by category",
    "Summary by type (income vs expense)",
    "Summary by month",
    "Summary by custom date range",
)
REDO_SORT_PROMPT = "Would you like to summarize something else?"
SUMMARY_NO_DATA = 'No transactions were found for "{selection}".'
SUMMARY_RETRY_PROMPT = "Would you like to try a different summary?"
SUMMARY_SELECTION_FALLBACK = "selection"
ENTER_MONTH_PROMPT = "Enter month (1-12): "
ENTER_YEAR_PROMPT = "Enter year (YYYY): "
ENTER_START_DATE_PROMPT = f"Enter start date ({DATE_FORMAT_HUMAN}): "
ENTER_END_DATE_PROMPT = f"Enter end date ({DATE_FORMAT_HUMAN}): "
INVALID_MONTH_MESSAGE = "Invalid month. Please enter a number between 1 and 12."
INVALID_YEAR_MESSAGE = "Invalid year. Please enter a four-digit year (e.g., 2025)."
DISPLAY_SUMMARY_PROMPT = "Press any character to return to the Summary hub."
SPECIAL_H1, SPECIAL_H2, SPECIAL_H3 = "Category", "Count", "Total"
INCOME = "Income"
EXPENSE = "Expense"
SUMMARY_FALLBACK_TITLE = "Summary"
TRANSACTIONS_ANALYZED_LABEL = "Transactions analyzed"

# Edit hub
EDIT_HUB_NAME = "Edit hub"
EDIT_HUB_OPTIONS = (
    "Edit a transaction",
    "Delete a transaction",
    "Add a new transaction",
    "View save",
)
ADD_TRANSACTION_PROMPT = "Add transaction"
EDIT_TRANSACTION_PROMPT = "Which transaction would you like to edit?"
SEL_ITEM_PROMPT = "Which field would you like to edit?"
NEW_VALUE_PROMPT = "Enter the new value:"
REDO_EDIT_TRANSACTION_PROMPT = "Would you like to edit another field in this transaction?"
ADD_ITEM_TO_SAVE = "Save these changes?"
EDIT_HUB_NO_RESULT = "1"
SELECTED_ITEM_LABEL = "Selected Item:"
ITEM_NUMBER_LABEL = "Item: {index}"
SELECTED_KEY_LABEL = "Selected key: {key}"
SELECTED_ITEM_FOR_DELETION = "Selected Item for deletion (Item {index}):"
DEL_TRANSACTION_PROMPT = "Which transaction would you like to delete?"
RETRY_DEL_PROMPT = "Would you like to select a different transaction?"
DEL_ANOTHER_PROMPT = "Would you like to delete another transaction?"
NO_MORE_TRANSACTIONS = "No more transactions."

# PDF import
PDF_IMPORT_HUB = "PDF Import"
PDF_METHOD_PROMPT_NEW_SAVE = "How would you like to create transactions?"
PDF_METHOD_PROMPT_ADD = "How would you like to add transactions?"
PDF_METHOD_OPTIONS = (
    "Manual entry",
    "Import from PDF statement",
)
PDF_SELECT_FILE = "Select a PDF file to import:"
PDF_CUSTOM_PATH = "Enter custom PDF path"
PDF_SELECT_PARSER = "Select a parser:"
PDF_PARSE_FAILED = "PDF parsing failed."
PDF_NO_TRANSACTIONS = "No transactions found in this PDF."
PDF_REVIEW_ITEM_LABEL = "Item {index}/{total}"
PDF_REVIEW_ACTIONS = "What would you like to do with this item?"
PDF_EDIT_FIELD = "Edit {field}"
PDF_EDIT_PROMPT = "Enter new value: "
PDF_SKIP_ITEM = "Skip this transaction"
PDF_ACCEPT_ITEM = "Accept and continue"
PDF_CANCEL_IMPORT = "Cancel import"
PDF_REVIEW_SUMMARY = "Accepted: {accepted} | Skipped: {skipped}"
PDF_CONFIRM_NEW_SAVE = "Create save with imported transactions?"
PDF_CONFIRM_ADD = "Add imported transactions to current save?"
PDF_IMPORT_CANCELED = "PDF import canceled."
PDF_FILE_NOT_FOUND = "File not found. Please try again."

# Undo/Redo hub
UNDOREDO_HUB_NAME = "Undo / Redo Menu"
UNDOREDO_HUB_OPTIONS = (
    "Undo last action",
    "Redo last action",
    "View current save",
)
NOTHING_TO_UNDO = "Nothing to undo or undo failed."
ACTION_UNDONE = "Action undone."
NOTHING_TO_REDO = "Nothing to redo or redo failed."
ACTION_REDONE = "Action redone."

# Validation and error text
ERROR_UNKNOWN_FIELD = "ERROR: Unknown field '{key}'."
ERROR_TYPE_MUST_BE_IE = "ERROR: Type must be I or E."
ERROR_EXPECTED_TYPE = "ERROR: Expected {dtype}."
ERROR_DATE_FORMAT = f"ERROR: Date must follow {DATE_FORMAT_HUMAN} (e.g. {DATE_EXAMPLE})."
ERROR_ENTER_NUMBER = "Please enter a number"
INVALID_TRANSACTION_TYPE = "Invalid type in: {name}; type: {type}"

# Sorting labels
FILTER_BY_KEY_VALUE_LABEL = "Filter by key, value"

# Main entry messages
EXITED_START = "Exited start"
EXITED_HUB = "Exited hub"
ANALYZE_HUB_INVALID_CHOICE = "analyze_hub: invalid choice"
EDIT_HUB_INVALID_CHOICE = "edit_hub: invalid choice"
SUMMARY_HUB_INVALID_CHOICE = "summary_hub: invalid choice"
PREHUB_TOO_MANY_FAILS = "Contact Dev - repeated load failures"
PREHUB_INVALID_INITIAL_CHOICE = "prehub: invalid initial choice"
MAIN_HUB_INVALID_CHOICE = "hub: invalid choice"



