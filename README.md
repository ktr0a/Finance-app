# Finance App - Version 2.0

## Overview

The Finance App is a modular Python-based personal finance tracker built around a structured “transaction” model and a hub-based CLI workflow.  
Version 2.0 introduces a **PDF import MVP** (currently focused on Austrian bank statement layouts) while keeping the core system stable and reusable for future UI/UX (FastAPI + frontend).

---

## Features (V2.0)

### ✅ Core Finance Tracking
- Store and manage transactions as structured entries:
  - `name`, `category`, `type`, `amount`, `date`
- Create, edit, delete, and view transactions via CLI hubs
- Filtering, sorting and summaries
- Works with a persistent JSON save file

### ✅ Undo / Redo + Backups
- Undo/redo stacks stored as JSON snapshots
- Session backups + restore functionality (through the hub workflow)

### ✅ PDF Import MVP (New in V2)
You can now import transactions from PDF statements:
- **During save creation (Prehub)**: create a new save from a PDF statement
- **During editing (Edit hub)**: add transactions from a PDF statement into an existing save
- **Full per-item review/edit flow**:
  - You step through every parsed transaction item
  - You can edit any field (especially category, which is not provided in the PDF)
  - You can skip individual items
  - Only confirmed items are imported

**Current limitation (MVP):**
- Parsing is layout-dependent and currently supports **Erste Bank statements (MVP)**.
- More banks / auto-detection / OCR fallback are planned.

---

## Project Structure (V2.0)

```

Finance_app/
core/                         # Core logic (engine + helpers)
engine.py                   # Engine API (persistence-owned ops) + calc/sum/sort utils
core_config.py              # definers/config init
models.py                   # Result + shared types
ports.py                    # Repository/History protocols
errors.py                   # Core error types

infra/                        # Storage implementation
storage_json.py             # JSON repository + undo/redo + backups

cli/                          # Hub-based CLI UI
cli.py                      # main CLI runner
helper.py                   # CLI input validation helpers
prettyprint.py              # formatted output helpers
prompts.py                  # re-export prompt/config constants
cli_hub_modules/            # all hub workflows (prehub, main hub, edit hub, ...)
pdf_import_hub.py         # PDF import UI flow (review/edit each item)

config/                       # Text + parameters + schema + storage config
text.py                     # user-facing text
params.py                   # formatting/constants (spacer chars etc.)
schema.py                   # date formats, definers schema
storage.py                  # save/backup path constants
calc_summary.py             # calc/summary config

pdf_handeling/                # PDF import system (MVP)
api.py                      # parser registry + parse_pdf boundary for CLI / future API
general_extract_rawdata.py  # word-box extraction from pdf (path-based)
parameter.py                # parsing parameters
erste_bank/
parser.py                 # Erste wrapper parser (path-based entrypoint)
erste_format_rawdata.py   # transaction segmentation / marker extraction
erste_manual_data_mapper.py # mapping to transaction dict + status

storage/                      # save + backups + undo/redo snapshot folders
main.py                       # entrypoint (hub workflow)
requirements.txt              # dependencies

```

---

## Installation

1) Clone the repository  
2) Create a virtual environment (recommended)  
3) Install dependencies:

```bash
pip install -r requirements.txt
```

---
## Running the App

From the project root:

```bash
python main.py
```

You will be guided through the hub-based CLI:

* load or create a save
* view/edit transactions
* analyze / summary tools
* undo/redo and backups
* PDF import (MVP)

---

## PDF Import (MVP) Usage

### Creating a new save from a PDF

* Start the app → choose **Create new save**
* Select **Import from PDF statement**
* Select the PDF file (rawdata folder or custom path)
* Select parser (Erste MVP)
* Review/edit every item → confirm → save created

### Adding PDF transactions to an existing save

* Load save → go to **Edit hub**
* Choose **Add transaction(s)**
* Select **Import from PDF**
* Review/edit every item → confirm → imported

---

## Notes / Known Limitations

* The PDF import is currently an MVP:

  * designed to be extendable via `pdf_handeling/api.py` parser registry
  * layout-dependent (Erste Bank supported as MVP)
* Category is not provided by the PDF and must be assigned manually during review.
* Relative storage paths expect you to run `python main.py` from the project root.

---

## License

MIT License. See `LICENSE`.

---

## Roadmap (Next Steps)

* Improve PDF pipeline:

  * additional bank layouts
  * stronger marker detection
  * OCR or Vision-LLM fallback for ambiguous cases
  * auto-detection across parsers
* FastAPI backend + frontend UI on top of the Engine API
* Import/export utilities and more analytics
