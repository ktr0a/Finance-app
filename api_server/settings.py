from __future__ import annotations

from pathlib import Path

from config.storage import SAVE_FILENAME, STORAGE_DIR_NAME

API_PORT = 8787

SAVE_DIR = Path(STORAGE_DIR_NAME)
SAVE_FILE_NAME = SAVE_FILENAME

# CORS is off by default. Set ENABLE_CORS = True if needed.
CORS_ORIGINS: list[str] = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]
ALLOWED_ORIGINS = CORS_ORIGINS
ENABLE_CORS = False
