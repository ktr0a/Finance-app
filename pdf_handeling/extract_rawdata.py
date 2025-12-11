import fitz

try:
    import pdf_handeling.parameter as parameter
except ImportError:
    import parameter

# (x0, y0, x1, y1, text, block_no, line_no, word_no)

def raw_extraction() -> list: # Extract text from pdf; round & nest by page
    document = fitz.open(f"{parameter.RAWDATA_DIR}\\{parameter.FILE_NAME}")
    total_wordlst = []

    for page_number, page in enumerate(document, start=1): #type: ignore
        rounded_page = []

        total_words_on_page = page.get_text("words")

        for word in total_words_on_page:
            rounded_words = _rounding_values(word)
            rounded_page.append(rounded_words)
        
        total_wordlst.append(list(rounded_page))

    return total_wordlst

def _rounding_values(word: tuple) -> list:
    x0, y0, x1, y1, text, block_no, line_no, word_no = word
    return [
        round(x0, parameter.ROUNDING_INT), round(y0, parameter.ROUNDING_INT),
        round(x1, parameter.ROUNDING_INT), round(y1, parameter.ROUNDING_INT),
        text, block_no, line_no, word_no
    ]
