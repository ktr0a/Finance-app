import unittest
from unittest import mock
from pathlib import Path
import tempfile

from cli.cli_hub_modules.main_hub import hub
import core.core_config as core_config

from cli.cli_hub_modules.calc_hub import calc_loop
import main
import core.storage as storage
import time


class CalcHubTests(unittest.TestCase):
    def setUp(self):
        self.sample_save = core_config.testin()

    def test_total_income_calculation(self):
        result = calc_loop(1, self.sample_save)
        self.assertTrue(result.startswith("Total Income: "))

    def test_total_expense_is_signed(self):
        result = calc_loop(2, self.sample_save)
        self.assertIn("Total Expense: -", result)


class MainFlowTests(unittest.TestCase):
    def test_run_cli_exits_when_start_returns_none(self):
        with mock.patch("main.start", return_value=None) as start_mock, \
             mock.patch("main.hub") as hub_mock, \
             mock.patch("builtins.print"):
            main.run_cli()

        start_mock.assert_called_once()
        hub_mock.assert_not_called()

    def test_run_cli_calls_hub_when_save_is_loaded(self):
        sample_save = {"foo": "bar"}
        with mock.patch("main.start", return_value=sample_save) as start_mock, \
             mock.patch("main.hub", return_value=None) as hub_mock, \
             mock.patch("builtins.print"):
            main.run_cli()

        start_mock.assert_called_once()
        hub_mock.assert_called_once_with(sample_save)


class UndoRedoTests(unittest.TestCase):
    def setUp(self):
        self.tmp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp_dir.cleanup)

        base = Path(self.tmp_dir.name)
        patchers = [
            mock.patch.object(storage, "MAIN_DATA_FILE", base / "storage/save.json"),
            mock.patch.object(storage, "BACKUP_DIR", base / "storage/backups/"),
            mock.patch.object(storage, "UNDO_DIR", base / "storage/undo_stack/"),
            mock.patch.object(storage, "REDO_DIR", base / "storage/redo_stack/"),
        ]

        for patcher in patchers:
            patcher.start()
            self.addCleanup(patcher.stop)

        self.undo_dir = storage.UNDO_DIR
        self.redo_dir = storage.REDO_DIR

    def test_undo_and_redo_round_trip(self):
        original = [{"id": 1, "amount": 100, "date": storage.DEFAULT_DATE}]
        updated = [{"id": 1, "amount": 50, "date": storage.DEFAULT_DATE}]

        storage.save(original)
        storage.cr_backup_lst(original, mode="undo", delbackup=False)
        storage.save(updated)

        status, data = storage.undo_action()
        self.assertTrue(status)
        self.assertEqual(data, original)

        redo_entries = list(self.redo_dir.glob(f"{storage.BACKUP_DATA_FILE_NAME}*.json"))
        self.assertGreaterEqual(len(redo_entries), 1)

        status, data = storage.redo_action()
        self.assertTrue(status)
        self.assertEqual(data, updated)


def main():
    try:
        import pdf_handeling.general_extract_rawdata as pdf_rawdata
        import pdf_handeling.erste_bank.erste_format_rawdata as pdf_format
        import pdf_handeling.parameter as pdf_parameter
    except ImportError:
        import rawdata as pdf_rawdata
        import format as pdf_format
        import parameter as pdf_parameter

    total_wordlst = pdf_rawdata.raw_extraction()
    markers = pdf_format.extract_markers(total_wordlst, pdf_parameter.MARKER_STR)
    valid_lst = pdf_format.extract_words_in_markers(
        total_wordlst,
        markers if markers != None else exit("Markers is empty"),
    )

    print(pdf_format._flatten_lst(valid_lst))

    transactions_lst = pdf_format.sort_to_transactions(valid_lst, markers)
    print(transactions_lst)

    newtransactions_lst, blacklst = pdf_format.delete_blacklist(transactions_lst)

    pdf_format.pretty_print_transactions(newtransactions_lst)

def asdfsd():
    total_wordlst = rd.raw_extraction()
    
    markers = f.extract_markers(total_wordlst, p.MARKER_STR)

    valid_lst = f.extract_words_in_markers(
        total_wordlst,
        markers if markers is not None else exit("Markers is empty"),
    )

    transactions_lst = f.sort_to_transactions(valid_lst, markers)
    print(transactions_lst)

    newtransactions_lst, blacklst = f.delete_blacklist(transactions_lst)

    print()
    print()
    print()
    print(newtransactions_lst)
    print()
    print()
    print()
    print(blacklst)

    date = f.find_dateformat_in_blacklst(blacklst)

    print("sigma")
    print()
    print(date)
    print()

    item = e_item()
    variance = p.VARIANCE

    status, a_value, t_value = mdm.amount_type_per_item(item[3], markers if markers is not None else exit())
    dstatus, d_value = mdm.date_per_item(dateword=item[2], amountword=item[2+1], yr=date)

    print()
    print(status)
    print()
    print(a_value)
    print(t_value)
    print("---")
    print(dstatus)
    print()
    print(d_value)


def mdm_on_eitem():
    print(mdm.name_main(e_item()))

    cleaned = mdm.name_main(e_item())
    print("CLEANED (per-line tokens):")
    print(cleaned)

    best = mdm.name_scoring_main(cleaned if cleaned is not None else [])
    print("BEST NAME:")
    print(best)

    item = e_item()
    validx1 = max(w[2] for w in item)  # rightmost x1 in this transaction
    markers = (0.0, 0.0, float(validx1), 0.0)

    mapped, st = mdm.map_transaction(item, markers=markers, yr="2025")

    print("MAPPED:")
    print(mapped)
    print("STATUS:")
    print(st)


if __name__ == "__main__":
    import pdf_handeling.erste_bank.erste_manual_data_mapper as mdm
    import pdf_handeling.general_extract_rawdata as rd
    import pdf_handeling.erste_bank.erste_format_rawdata as f
    import pdf_handeling.parameter as p

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



