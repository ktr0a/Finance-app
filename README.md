# Finance Tracker CLI - Version 1.0.0

A simple, modular command-line finance tracker written in Python.  
This V1 release includes save/load functionality, transaction entry, and two basic calculations (total income and total expense).

---

## Features (V1)

### 🧾 Transaction Handling
- Create a new save file  
- Load an existing save file  
- Store transactions as dictionaries:
  - `name` *(str)*
  - `category` *(str)*
  - `type` - **I** for income, **E** for expense
  - `amount` *(float)*

### Calculations
- **Total Income**
- **Total Expense**

### Save System
- Saves all transactions to `save.json`  
- Loads transactions from `save.json`  
- Automatically handles missing/empty save file  
- Clean JSON formatting via `storage.py`  

### CLI Interface
- Interactive menus  
- Input validation (numbers + yes/no)  
- Pretty-printed transactions for readability  
- Modular architecture (easy to extend later)

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

## Roadmap (Future Versions)

### Planned for future releases:
- Net balance (income - expense)
- Totals per category
- Monthly and yearly summaries
- Edit/remove individual transactions
- Sorting and filtering options
- Autosave on exit
- Multiple save files
- More detailed financial statistics

---

## License

MIT License

---

## Author
Created by ktr0a
