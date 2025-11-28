# Finance Tracker CLI - Version 1.0.0

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

```text
Finance-App/
│
├── main.py          # Entry point: start → load/create → hub
├── cli.py           # All interactive CLI logic
├── utils.py         # Calculation utilities (total income/expense)
├── storage.py       # JSON save/load logic
├── parameters.py    # Data schema and default definitions
└── save.json        # Auto-created: stores transaction data
```

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
Enter transactions, view them, and run calculations — all via clean terminal prompts.

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
Created by ktr0a
