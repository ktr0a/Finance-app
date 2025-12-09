import fitz
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

CATEGORY_VARIANCE = 3.0



# (x0, y0, x1, y1, text, block_no, line_no, word_no)



def raw_extraction() -> list:
    try:
        import pdf_handeling.format as pdf_format
    except ImportError:
        import format as pdf_format

    doc = fitz.open(f"{RAWDATA_DIR}\\{FILE_NAME}")
    total_wordlst = []


    for page_number, page in enumerate(doc, start=1): 
        rounded_page = []

        total_words_on_page = page.get_text("words")

        for word in total_words_on_page:
            rounded_words = pdf_format._rounding_values(word)
            rounded_page.append(rounded_words)
        
        total_wordlst.append(list(rounded_page))

    return total_wordlst



if __name__ == "__main__":
    try:
        import pdf_handeling.format as pdf_format
    except ImportError:
        import format as pdf_format

    total_wordlst = raw_extraction()
    markers = pdf_format.extract_markers(total_wordlst, MARKER_STR)
    valid_lst = pdf_format.extract_words_in_markers(total_wordlst, markers if markers != None else exit("Markers is empty"))

    print(pdf_format._flatten_lst(valid_lst))

    transactions_lst = pdf_format.sort_to_transactions(valid_lst, markers)
    print(transactions_lst)

    newtransactions_lst = pdf_format.delete_blacklist(transactions_lst)

    pdf_format.pretty_print_transactions(newtransactions_lst)
