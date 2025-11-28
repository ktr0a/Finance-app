# Finance Tracker CLI - Version 1.1

A modular command-line finance tracker written in Python.
Version 1.1 extends the original release with editing, deletion, filtering, and expanded calculations, with a strong focus on stability and input validation.

---

## Features (v1.1)

### Transaction Handling

* Create a new save file
* Load an existing save file
* Add transactions to an existing save
* Edit individual transaction fields
* Delete single or multiple transactions
* Transactions are stored as dictionaries with:

  * `name` (str)
  * `category` (str)
  * `type` (“I” for income, “E” for expense)
  * `amount` (float)

---

### Analysis and Calculations

Calculations can be performed on:

* The full dataset, or
* A filtered subset

Available calculations:

* Total income
* Total expense
* Net balance
* Number of transactions
* Average transaction amount
* Maximum transaction
* Minimum transaction

---

### Filtering

Transactions can be filtered by:

* Name
* Category
* Type
* Amount

The user can retry filters and choose whether to analyze the filtered dataset or return to the full one.

---

### Save System

* Transactions are saved to `save.json`
* Data is loaded from `save.json`
* Missing, empty, and corrupted save files are detected
* All edits and deletions persist immediately

---

### CLI Interface

* Interactive menu-based navigation
* Validation for numeric input, yes/no prompts, and transaction fields
* Pretty-printed transaction output
* All modifying operations follow a strict return contract:

  * `None` means no change
  * `save` means data was modified and persisted

---

## Changes Since v1.0

* Transactions can now be edited after creation
* Transactions can be deleted safely (single or multiple)
* New transactions can be added to an existing save
* Transactions can be filtered before analysis
* Additional calculations were added
* Input validation and exit handling were hardened
* CLI prompts were cleaned up for clarity

---


## Project Structure

* `main.py` - program entry point
* `core/`

  * `config.py` - schema and default definitions
  * `calc_utils.py` - calculation logic
  * `sort_utils.py` - filtering and dataset operations
  * `storage.py` - JSON save/load system
* `cli/`

  * `cli.py` - main CLI logic
  * `helper.py` - validation and helpers
  * `prettyprint.py` - terminal formatting
  * `prompts.py` - user-facing text
* `save.json` - auto-created transaction storage

---

## Running the Program

1. Clone the repository
2. Run `python main.py`
3. Follow the CLI to load or create a save, then view, analyze, edit, or delete transactions

---

## Roadmap

* V1:
  * Date Support
    * Time-spam summaries (monthly, yearly, custom)
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

ktr0a
