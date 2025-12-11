from pathlib import Path

PARENT_DIR_NAME = "pdf_handeling"
PARENT_DIR = Path(PARENT_DIR_NAME)

RAWDATA_DIR_NAME = "rawdata"
FINAL_DIR_NAME = "final"

FILE_NAME = "1.pdf"

RAWDATA_DIR = PARENT_DIR / RAWDATA_DIR_NAME
FINAL_DIR = PARENT_DIR / FINAL_DIR_NAME

ROUNDING_INT = 2

MARKER_STR = "Kontostand"
SPECIFIC_STR = "Kontostand"

BLACKLIST = (
    "Kontostand",
    "***",
)

VARIANCE = 3.0
