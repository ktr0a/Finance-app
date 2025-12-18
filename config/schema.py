# Domain and data model constants.
# Used by core/core_config & many logic operations. Changing things will most likely break things.

DEFINERS = (
    ("name", str),
    ("category", str),
    ("type", str),
    ("amount", float),
    ("date", str),  # EU format: DD.MM.YYYY
)

TRANSACTION_TYPES = ("I", "E")

DATE_FORMAT = "%d.%m.%Y"
DATE_FORMAT_HUMAN = "DD.MM.YYYY"
DATE_EXAMPLE = "05.01.2025"

AMOUNT_OF_BACKUPS = 5
AMOUNT_OF_CONSECUTIVE_PREHUB_FAILS = 5
