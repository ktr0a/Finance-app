try:
    import pdf_handeling.general_extract_rawdata as rd
    import pdf_handeling.erste_bank.erste_format_rawdata as f
    import pdf_handeling.parameter as p
except ImportError:
    import pdf_handeling.general_extract_rawdata as rd
    import pdf_handeling.erste_bank.erste_format_rawdata as f
    import parameter as p


def run_extraction_demo() -> None:
    total_wordlst = rd.raw_extraction()
    markers = f.extract_markers(total_wordlst, p.MARKER_STR)
    valid_lst = f.extract_words_in_markers(
        total_wordlst,
        markers if markers is not None else exit("Markers is empty"),
    )

    print(f._flatten_lst(valid_lst))

    transactions_lst = f.sort_to_transactions(valid_lst, markers)
    print(transactions_lst)

    newtransactions_lst, blacklst = f.delete_blacklist(transactions_lst)

    f.pretty_print_transactions(newtransactions_lst)

def example_item() -> list:
    item = [
        [47.34, 61.77, 125.34, 74.26, '1045047095378', 6, 0, 0], 
        [131.34, 61.77, 167.34, 74.26, 'PAYPAL', 6, 0, 1], 
        [446.34, 61.77, 470.34, 74.26, '2509', 6, 1, 0], 
        [540.34, 61.77, 582.34, 74.26, '415,10-', 6, 2, 0], 
        [59.34, 71.77, 95.34, 84.26, 'PayPal', 6, 3, 0], 
        [101.34, 71.77, 149.34, 84.26, '(Europe)', 6, 3, 1], 
        [155.34, 71.77, 173.34, 84.26, 'S.a', 6, 3, 2], 
        [179.34, 71.77, 203.34, 84.26, 'r.l.', 6, 3, 3], 
        [209.34, 71.77, 221.34, 84.26, 'et', 6, 3, 4], 
        [227.34, 71.77, 251.34, 84.26, 'Cie,', 6, 3, 5], 
        [257.34, 71.77, 269.34, 84.26, 'S.', 6, 3, 6], 
        [59.34, 83.17, 167.34, 95.66, 'MDID:5SR22259HPEXW', 6, 4, 0], 
        [59.34, 94.57, 137.34, 107.06, '1045047095378', 6, 5, 0], 
        [143.34, 94.57, 179.34, 107.06, 'PAYPAL', 6, 5, 1]]
    return item

if __name__ == "__main__":
    run_extraction_demo()

