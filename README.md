# Finance Tracker CLI – Version 1.2

A modular command-line finance tracker written in Python.
Version 1.2 introduces **date-aware transactions** and a **summary hub** for high-level overviews, building on the stable editing, deletion, and filtering system from v1.1.

---

## Features (v1.2)

### Transaction Handling

* Create a new save file
* Load an existing save file
* Add transactions to an existing save
* Edit individual transaction fields
* Delete single or multiple transactions

Transactions are stored as dictionaries with:

* `name` (str)
* `category` (str)
* `type` (“I” for income, “E” for expense)
* `amount` (float)
* `date` (str, `DD.MM.YYYY`, EU format)

All fields are validated through shared input validators before being accepted.

---

### Analysis and Calculations

Calculations can be performed on:

* The full dataset, or
* A filtered subset

Available calculations (unchanged core set):

* Total income
* Total expense
* Net balance
* Number of transactions
* Average transaction amount
* Maximum transaction
* Minimum transaction

Results are formatted consistently (money / integer) and printed in a clean, readable format.

---

## Summary Hub (New in v1.2)

Version 1.2 adds a dedicated **Summary Hub** inside the calculation menu, providing higher-level views on your data.

Available summaries:

* **All-time summary**

  * Applies the core calculations to the entire dataset.

* **General category overview**

  * Counts and totals per category
  * Sorted by total amount (descending)
  * Includes overall net balance

* **General income vs expense overview**

  * Separate sections for income and expense
  * Count and total per type
  * Includes overall net balance

* **Summary by key–value pair**

  * By name
  * By category
  * By type (income vs expense)
    Each mode filters transactions first, then applies the core calculations to the subset.

* **Summary by month**

  * Uses the `date` field to summarize a specific month and year
  * Automatically derives the date range from `01.mm.yyyy` to the last day of the month

* **Summary by custom date range**

  * User supplies start and end dates (`DD.MM.YYYY`)
  * Only transactions within the inclusive range are analyzed

When a summary would contain **no data**, the CLI warns the user and offers to retry with different parameters instead of printing an empty summary.

---

## Date Support (New in v1.2)

* Each transaction now includes a `date` field (`DD.MM.YYYY`, EU format).
* Date input is validated using the same shared validation layer as other fields.
* The date is used for:

  * Filtering (via the general filter system)
  * **Summary by month**
  * **Summary by custom date range**

This is the first step of the planned time-based analytics from the roadmap.

---

## Filtering

Transactions can be filtered by:

* Name
* Category
* Type
* Amount
* Date (`DD.MM.YYYY`)

The user can:

* Retry filters when no match is found
* Choose whether to analyze the filtered dataset or return to the full one
* Reuse the filtered subset in both the standard **Calculations Hub** and the **Summary Hub**

---

## Save System

* Transactions are saved to `storage/save.json`
* Data is loaded from `storage/save.json`
* Missing, empty, and corrupted save files are detected
* All edits and deletions persist immediately
* The new `date` field is stored alongside the existing transaction fields

---

## CLI Interface

* Interactive, menu-based navigation for:

  * Start (load/create)
  * Analyze (filter + calculations + summaries)
  * View
  * Edit / delete / add transactions
* Dedicated **Summary Hub** within the calculation menu
* Shared validation for numeric input, yes/no prompts, and all transaction fields (including dates)
* Pretty-printed transaction lists and formatted summary views:

  * Category overview table with aligned columns
  * Income vs expense breakdown sections
* All modifying operations follow the same contract:

  * `None` → no change
  * Updated list → save is modified and persisted

---

## Changes Since v1.1

* Added `date` to the transaction schema (EU format `DD.MM.YYYY`)
* Integrated date validation into creation, editing, and filtering
* Implemented a **Summary Hub** with:

  * All-time summary
  * General category overview
  * General income vs expense overview
  * Summary by name/category/type
  * Summary by month
  * Summary by custom date range
* Added specialized pretty-printing for category and income/expense summaries
* Improved handling when summaries or filters produce no matching data
* Kept the v1.1 editing, deletion, and filtering behavior while routing it through shared validators and new summary logic

---

## Project Structure

```text
Finance-App/
|-- main.py                # Entry point: start + load/create + hub
|
|-- core/
|   |-- config.py          # Data schema, defaults, and init helpers
|   |-- storage.py         # JSON save/load logic
|   |-- calc_utils.py      # Basic calculations and formatting helpers
|   |-- sort_utils.py      # Filtering and sorting utilities
|   `-- sum_utils.py       # Summary modes (all-time, category, date-range, etc.)
|
|-- cli/
|   |-- cli.py             # Main CLI flow (start, hub, analysis, edit)
|   |-- helper.py          # Input validation and shared CLI helpers
|   |-- prettyprint.py     # Output formatting and terminal helpers
|   `-- prompts.py         # All user-facing strings and prompts
|
`-- storage/
    |-- save.json          # Auto-created: stores transaction data
    |-- backups/           # Regular backups
    |-- undo_stack/        # Undo history
    `-- redo_stack/        # Redo history
```


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
