# Finance Tracker CLI – Version 1.3

A modular command-line finance tracker written in Python.

Version 1.3 keeps all v1.2 features (date-aware transactions, summary hub, filtering, etc.) and adds a more robust save system: a dedicated `storage/` folder, multiple timestamped backups, and a full undo/redo workflow. Internally, configuration has been centralized into a `config/` package to make future changes (like PDF OCR) easier.

---

## Features (v1.3)

### Transaction Handling

- Create a new save file
- Load an existing save file
- Add transactions to an existing save
- Edit individual transaction fields
- Delete single or multiple transactions

Transactions are stored as dictionaries with:

- `name` (str)
- `category` (str)
- `type` (`"I"` for income, `"E"` for expense)
- `amount` (float)
- `date` (str, `DD.MM.YYYY`, EU format)

All fields are validated through shared input validators before being accepted.

---

### Analysis and Calculations

Calculations can be performed on:

- The full dataset, or
- A filtered subset

Available calculations:

- Total income
- Total expense
- Net balance
- Number of transactions
- Average transaction amount
- Maximum transaction
- Minimum transaction

Results are formatted consistently (money / integer) and printed in a readable format.

---

## Summary Hub

The Summary Hub (introduced in v1.2) is still the main place for high-level views on your data.

Available summaries:

- **All-time summary**
  - Applies the core calculations to the entire dataset.

- **General category overview**
  - Counts and totals per category
  - Sorted by total amount (descending)
  - Includes overall net balance

- **General income vs expense overview**
  - Separate sections for income and expense
  - Count and total per type
  - Includes overall net balance

- **Summary by key–value pair**
  - By name
  - By category
  - By type (income vs expense)  
  Each mode filters transactions first, then applies the core calculations to the subset.

- **Summary by month**
  - Uses the `date` field to summarize a specific month and year
  - Automatically derives the date range from `01.mm.yyyy` to the last day of the month

- **Summary by custom date range**
  - User supplies start and end dates (`DD.MM.YYYY`)
  - Only transactions within the inclusive range are analyzed

When a summary would contain no data, the CLI warns the user and offers to retry with different parameters instead of printing an empty summary.

---

## Date Support

- Each transaction includes a `date` field (`DD.MM.YYYY`, EU format).
- Date input is validated using the same shared validation layer as other fields.
- The date is used for:
  - Filtering (via the general filter system)
  - Summary by month
  - Summary by custom date range

---

## Filtering

Transactions can be filtered by:

- Name
- Category
- Type
- Amount
- Date (`DD.MM.YYYY`)

The user can:

- Retry filters when no match is found
- Choose whether to analyze the filtered dataset or return to the full one
- Reuse the filtered subset in both the standard Calculations Hub and the Summary Hub

---

## Save System (Updated in v1.3)

The save logic has been reworked around a dedicated `storage/` folder:

- **Main save**
  - Primary data lives in `storage/save.json`.
  - Missing, empty, and corrupted saves are detected.
  - All edits and deletions persist immediately once confirmed.

- **Backups**
  - Backups are stored in `storage/backups/` as timestamped JSON files  
    (`save_backup_YYYYMMDD_HHMMSS_ffffff.json`).
  - Old backups are pruned based on a configurable limit.
  - From the start hub you can restore directly from the latest backup.
  - From the main hub you can:
    - Create a backup on demand
    - Restore from previous backups

These backups are also used internally by the undo/redo feature.

---

## Undo / Redo Hub (New in v1.3)

Version 1.3 introduces a dedicated **Undo/Redo** hub in the main menu.

- Every time a mutating operation is performed (edit, add, delete), the previous state is stored in the **undo** stack.
- Using the Undo option:
  - The current state is pushed to the redo stack.
  - The most recent undo snapshot becomes the active save.
- Using the Redo option:
  - The current state is pushed back to the undo stack.
  - The most recent redo snapshot is restored.

Stacks are stored under:

- `storage/undo_stack/`
- `storage/redo_stack/`

Undo/redo history is session-based: stacks are cleared when a save is (re)loaded so you don’t accidentally reuse stale history from earlier runs.

---

## CLI Interface

- Interactive, menu-based navigation for:
  - Start (load, restore from latest backup, or create)
  - Analyze (filter + calculations + summaries)
  - View
  - Edit / delete / add transactions
  - Manage backups
  - Undo / redo changes

- Shared validation for:
  - Numeric input
  - Yes/no prompts
  - All transaction fields (including dates)

- Pretty-printed transaction lists and formatted summary views:
  - Category overview table with aligned columns
  - Income vs expense breakdown sections

All modifying operations follow the same contract:

- `None` → no change
- Updated list → save is modified and persisted

---

## Changes Since v1.2

- Introduced a **storage-based save layout**:
  - `storage/save.json`
  - `storage/backups/`
  - `storage/undo_stack/`
  - `storage/redo_stack/`

- Added a **manual backup flow**:
  - Create backup from the main hub
  - Restore from latest or earlier backups

- Implemented a **session-based undo/redo system** using snapshot files.

- Centralized configuration into a new `config/` package:
  - `config.schema` – transaction schema, date format, global parameters
  - `config.storage` – storage paths and backup naming
  - `config.calc_summary` – calculation labels, summary templates, formatting modes
  - `config.text` – user-facing strings and prompts
  - `config.style` – basic CLI styling constants

- Fixed smaller issues around stack clearing and tightened tests for backup/undo behavior.

The v1.2 date support, filtering, and summary features remain unchanged.

---

## Project Structure (v1.3)

```text
Finance-app/
│
├── main.py               # Entry point: start → load/create/restore → hub
│
├── config/               # Centralized configuration and text
│   ├── schema.py         # Data schema, date format, core parameters
│   ├── storage.py        # Storage layout and backup naming
│   ├── calc_summary.py   # Calc labels, summary templates, formatting modes
│   ├── text.py           # All user-facing strings and prompts
│   ├── style.py          # Basic CLI styling constants
│   └── __init__.py
│
├── core/
│   ├── core_config.py    # Init helpers and demo data
│   ├── storage.py        # JSON save/load, backups, undo/redo stacks
│   ├── calc_utils.py     # Basic calculations and formatting helpers
│   ├── sort_utils.py     # Filtering utilities
│   └── sum_utils.py      # Summary modes (all-time, category, date-range, etc.)
│
├── cli/
│   ├── cli.py            # Top-level CLI flow (start, hubs)
│   ├── helper.py         # Input validation and shared CLI helpers
│   ├── prettyprint.py    # Output formatting and terminal helpers
│   ├── prompts.py        # Thin wrapper importing text from config.text
│   └── cli_hub_modules/  # Individual hub implementations
│
├── storage/              # Runtime data (auto-created)
│   ├── save.json         # Main save file
│   ├── backups/          # Timestamped backups
│   ├── undo_stack/       # Undo snapshots
│   └── redo_stack/       # Redo snapshots
│
└── test.py               # Basic integration / behavior tests

---

## Installation & Running

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd Finance-App
```

### 2. Run the program

```bash
python main.py
```

### 3. Use the CLI prompts

Choose between loading an existing save or creating a new one.
Enter dated transactions, optionally filter them, run basic calculations, and explore the new Summary Hub for higher-level overviews.

---

## Roadmap

* V1:

  * Date Support

    * Time-span summaries (monthly, yearly, custom)
    * Trend analysis over time
  * Category Expansion

    * Define categories
    * Select predefined categories
    * Calculations per category
  * Save Expansion

    * Undo/Redo support
    * (Automatic) Backups
    * Multiple Profiles
    * CSV import/export
  * Search functionality

    * Free-text search across all fields
    * Field-specific search
    * Case-insensitive partial matching

* Future versions:

  * PDF analysis (using OCR or similar)
  * GUI version

---

## License

MIT License

---

## Author

Created by ktr0a
