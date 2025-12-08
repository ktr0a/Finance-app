# Sorting utilities
from config.text import FILTER_BY_KEY_VALUE_LABEL

from core.storage import load

def filter_save(filterby_key, filterby_value, old_save) -> list:
    filtered_save = []

    for item in old_save:
        if filterby_key not in item:
            continue

        item_value = item[filterby_key]

        # Case-insensitive comparison for str
        if isinstance(item_value, str) and isinstance(filterby_value, str):
            if item_value.lower() == filterby_value.lower():
                filtered_save.append(item)

        # Exact comparison for other dtypes
        else:
            if item_value == filterby_value:
                filtered_save.append(item)

    return filtered_save


sort_util_func = [
    (FILTER_BY_KEY_VALUE_LABEL, filter_save),
]

if __name__ == "__main__":
    _, save_data = load()
    sortby_key = "category"
    sortby_value = "Food"
    print(filter_save(sortby_key, sortby_value, save_data or []))
