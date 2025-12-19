from pathlib import Path

import pymupdf

try:
    import finance_app.infra.pdf.parameter as parameter
except ImportError:
    import parameter

# (x0, y0, x1, y1, text, block_no, line_no, word_no)

def raw_extraction(pdf_path: str | None = None) -> list: # Extract text from pdf; round & nest by page
    if pdf_path is None:
        path = parameter.RAWDATA_DIR / parameter.FILE_NAME
    else:
        path = Path(pdf_path)

    document = pymupdf.open(str(path))
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

