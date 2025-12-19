# API Quickstart

## Run locally

```bash
python scripts/run_api.py
```

Open docs at `http://127.0.0.1:8787/docs`.

## Example requests

Create a save:

```bash
curl -X POST http://127.0.0.1:8787/saves \
  -H "Content-Type: application/json" \
  -d "{\"name\":\"demo_save\"}"
```

Add a transaction:

```bash
curl -X POST http://127.0.0.1:8787/saves/demo_save/transactions \
  -H "Content-Type: application/json" \
  -d "{\"name\":\"Coffee\",\"category\":\"food\",\"type\":\"E\",\"amount\":3.5,\"date\":\"01.01.2025\"}"
```

List transactions (no limit):

```bash
curl "http://127.0.0.1:8787/saves/demo_save/transactions?limit=0"
```

PDF preview:

```bash
curl -X POST http://127.0.0.1:8787/pdf/preview \
  -F "file=@/path/to/statement.pdf" \
  -F "parser=auto"
```
