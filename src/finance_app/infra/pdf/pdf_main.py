
def erste_main() -> list | None:
    import erste_bank.erste_manual_data_mapper as mdm
    import general_extract_rawdata as rd
    import erste_bank.erste_format_rawdata as f
    import parameter as p

    total_wordlst = rd.raw_extraction()

    markers = f.extract_markers(total_wordlst, p.MARKER_STR)

    valid_lst = f.extract_words_in_markers(
        total_wordlst,
        markers if markers is not None else exit("Markers is empty"),
    )

    transactions_lst = f.sort_to_transactions(valid_lst, markers)

    word_transactionlst, blacklst = f.delete_blacklist(transactions_lst)

    datestr = f.find_dateformat_in_blacklst(blacklst)


    if p.DEBUG_FLAG == True:
        print("P1:")
        print(word_transactionlst)
        print()
        print()
        print(datestr)
        print("P1: END")

    mapped = []

    for item in word_transactionlst:

        mappeditem = mdm.map_transaction(item, markers, datestr)
        if p.DEBUG_FLAG is True: 
            print(item)
            print()
            print()
        mapped.append(mappeditem)

    if p.DEBUG_FLAG is True: print(mapped)

    return mapped if mapped is not None else None

