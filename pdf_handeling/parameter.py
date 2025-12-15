from pathlib import Path
import re

PARENT_DIR_NAME = "pdf_handeling"
PARENT_DIR = Path(PARENT_DIR_NAME)

RAWDATA_DIR_NAME = "rawdata"

FILE_NAME = "bank2.pdf"

RAWDATA_DIR = PARENT_DIR / RAWDATA_DIR_NAME

ROUNDING_INT = 2

_THOUSANDS_EU = re.compile(r"^\s*\d{1,3}(\.\d{3})+(,\d{2})\s*[-+]?\s*$")
_MONEY_EU     = re.compile(r"^\s*[-+]?\d+([.,]\d{2})\s*[-+]?\s*$")

MARKER_STR = "Kontostand"
SPECIFIC_STR = "Kontostand"

BLACKLIST = (
    "Kontostand",
    "***",
)

VARIANCE = 3.0
EXTRA_MARGIN = 15.0 # is right side function

NAME_MAPPING_BLACKLIST = (
    "MDID:",
    "NDT:",
    "E-COMM",
    "SPESEN:",
)


# ----------------------------
# Name scoring configuration
# ----------------------------

# Weighted punctuation costs (higher = more suspicious)
PUNCT_CHARS = (
    (".", 1.0),
    (",", 1.0),
    ("-", 1.2),
    ("&", 1.3),

    ("/", 1.8),
    ("+", 1.8),
    ("'", 1.5),
    ("\"", 1.6),

    (":", 2.2),
    (";", 2.2),
    ("=", 2.5),
    ("_", 2.8),

    ("(", 3.5),
    (")", 3.5),
    ("[", 3.5),
    ("]", 3.5),
    ("{", 4.0),
    ("}", 4.0),

    ("@", 4.5),
    ("#", 4.5),
    ("%", 4.0),
    ("*", 4.0),
    ("^", 4.0),
    ("~", 3.8),
    ("`", 3.8),
    ("|", 4.0),
    ("\\", 4.2),

    ("<", 5.0),
    (">", 5.0),
)

# Common legal/company-form tokens that appear in merchant descriptors
# IMPORTANT: These should be compared against NORMALIZED tokens (lowercase, stripped punctuation).
LEGAL_TOKENS = {
    # German / Austrian
    "gmbh", "ag", "og", "kg", "gesmbh",

    # International
    "ltd", "limited", "inc", "llc", "plc", "corp", "co", "company",

    # French / Luxembourg-ish fragments often seen with PayPal etc.
    "sa", "s.a", "sarl", "s.a.r.l", "s.a.r.l.", "rl", "r.l", "r.l.", "cie", "et",
}

# Global scoring weights (tunable)
NAME_SCORING_WEIGHTS = {
    # PLUS
    "letters_bonus_per_char": 0.6,      # reward letters
    "sweetspot_wordcount_bonus": 2.0,   # reward typical merchant word counts
    "avg_token_len_bonus": 1.0,         # reward readable tokens

    # MINUS
    "punct_weight_multiplier": 0.5,     # scales PUNCT_CHARS sum
    "short_token_penalty": 2.5,         # tokens <= 2 chars (after normalization)
    "digit_token_penalty": 4.0,         # any digits in token
    "long_digit_id_penalty": 30.0,      # tokens that are mostly digits and very long
    "legal_token_penalty": 1.5,         # penalize each LEGAL token
    "url_like_penalty": 20.0,           # heavy penalty if URL/email indicators present
}

# Output shaping: 1 => "paypal"; 2 => "paypal europe"; 3 => allow "paypal europe services", etc.
NAME_OUTPUT_MAX_TOKENS = 3

# Safety net: remove a line like ["2509"] (DDMM) if it appears in name candidates
NAME_DROP_DATE_LIKE_LINES = True

# Flag for: Write print() debugs within mdm.py
DEBUG_FLAG = False