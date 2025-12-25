---
description: Start the Finance App Backend and Frontend
---

# Start Finance App Servers

// turbo-all

1. Start the Backend API:
```powershell
$env:PYTHONPATH = "src"; python scripts/run_api.py
```

2. Start the Frontend (Streamlit):
```powershell
$env:PYTHONPATH = "src"; streamlit run frontend_streamlit/app.py 
```