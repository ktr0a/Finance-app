#!/usr/bin/env bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FRONT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
ROOT_DIR="$(cd "${FRONT_DIR}/.." && pwd)"

cd "${ROOT_DIR}"
python scripts/run_api.py &
BACK_PID=$!

cd "${FRONT_DIR}"
streamlit run app.py

kill $BACK_PID
