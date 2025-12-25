# Finance App – Version 3.0

## Overview

The Finance App is a **modular, engine-first personal finance system** written in Python.
It is built around a **stable transaction core** that is **fully decoupled from any user interface**, allowing multiple frontends (CLI, Streamlit, FastAPI) to be layered on top **without modifying core logic**.

Version 3.0 marks a **structural milestone** rather than a feature-only update:
the project is now organized around a **frozen core engine** with thin adapters on top.

---

## Design Goals (V3)

Version 3.0 was designed with the following constraints in mind:

* **Single source of truth** for all financial logic
* **No UI-specific logic** inside the core
* **Backend-first architecture** suitable for long-term maintenance
* **Frontend-agnostic** (CLI, Streamlit, web UI can coexist)
* **Future-proof API surface** (FastAPI-ready without refactors)

This version is intended to be **stable enough to never touch the core again**, even as UIs evolve.

---

## Architecture Overview (V3)

```
Finance_app/
│
├─ core/                # Engine (pure business logic)
│   ├─ transactions/
│   ├─ filters/
│   ├─ summaries/
│   ├─ validation/
│   └─ state/
│
├─ infra/               # Infrastructure & IO
│   ├─ storage/
│   ├─ backups/
│   ├─ pdf_import/
│   └─ config/
│
├─ cli/                 # CLI adapter (thin layer)
│
├─ frontend_streamlit/  # Streamlit frontend (optional)
│
├─ api/                 # FastAPI adapter (future-ready)
│
└─ app.py / main.py     # Entry points
```

### Key Principle

> **The core does not know how it is being used.**
> It only knows *what* to compute, validate, or mutate.

---

## Features (V3.0)

### Core Finance Engine

* Fully isolated **transaction engine**
* Explicit data model:

  * `name`, `category`, `type`, `amount`, `date`
* Deterministic behavior (no hidden state)
* Validation and normalization handled centrally

### Filtering & Summaries (Engine-Level)

* Category, type, date, and amount filtering
* Summary calculations performed **inside the core**
* Identical results across all frontends

### Undo / Redo & Backups

* Snapshot-based undo/redo stacks
* Persistent JSON backups
* Infrastructure logic separated from business logic

### PDF Import (Engine-Safe)

* PDF parsing lives in `infra/`
* Extraction → normalization → engine ingestion
* No PDF assumptions inside the core

### Multi-Frontend Support

* CLI remains fully functional
* Streamlit frontend supported
* FastAPI adapter scaffolded for future web UI
* No duplicated business logic between UIs

---

## What Changed from V2 → V3

### Structural Changes

* Removed hub-centric assumptions from the core
* Introduced **engine-first workflow**
* Eliminated UI-driven control flow inside logic
* Reduced implicit coupling between files

### What Stayed the Same

* Transaction semantics
* Save file format
* Undo/redo behavior
* PDF import MVP behavior

---

## Stability & Freezing Policy

The following layers are considered **frozen** in V3:

* `core/`
* transaction schemas
* summary logic
* filtering semantics

Future work should only involve:

* new frontends
* better UX
* new adapters
* visualization layers

---

## Usage

### CLI

```bash
python app.py
```

### Streamlit

```bash
streamlit run frontend_streamlit/app.py
```

(FastAPI entry point is prepared but not required for normal usage.)

---

## Development Philosophy

This project is intentionally **over-structured for its current size**.

That is a feature.

The goal is to:

* demonstrate clean system boundaries
* allow aggressive frontend iteration
* prevent logic drift between interfaces
* enable long-term extension without rewrites

---

## Versioning

* **V1** – Monolithic CLI prototype
* **V2** – Feature-complete CLI + PDF import MVP
* **V3** – Engine-first architecture, UI-agnostic core (current)

---

## License

MIT License. See `LICENSE`.

## Additional notes (25.12.2025)

This project has been in development for a while and has reached a stable, real mvp. I first started this project back in November as something to get back into Coding and SWE - and within that short time I went from barely remembering the basic syntax of Python to achieving a top 5% placement in the 41st School CCC and an honourable mention in the December 2025 GDG AI Hackathon. 

I might continue this project in the future, depending on my future goals, interests and time. If I do, I plan to add new features and improve the user experience - turning it into a full fledged, commercially ready personal finance management system, not just a quickly made mvp (basically an app that people would actuallly use). I would probably mainly focus on rebuilding the frontend with react and adding better support for the pdf wizard.

However for now, I plan on shifting my focus to other fields - in particular, I plan on learning, revising and studying math and physics to prepare for the first year of university.

I will try to update this project from time to time, but I cannot promise anything.

---