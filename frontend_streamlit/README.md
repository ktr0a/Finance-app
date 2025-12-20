# Streamlit Frontend

## Install dependencies

```bash
pip install -r frontend_streamlit/requirements.txt
```

## Run backend (separately)

```bash
python scripts/run_api.py
```

## Run frontend

```bash
streamlit run frontend_streamlit/app.py
```

## Run with helper scripts

The helper scripts are robust to the current working directory, but it is still recommended to run them directly.

```bash
bash frontend_streamlit/scripts/run_local.sh
```

```powershell
powershell -ExecutionPolicy Bypass -File frontend_streamlit/scripts/run_local.ps1
```
