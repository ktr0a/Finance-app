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
        import pdf_handeling.rawdata as pdf_rawdata
        import pdf_handeling.format as pdf_format
    except ImportError:
        import rawdata as pdf_rawdata
        import format as pdf_format

    total_wordlst = pdf_rawdata.raw_extraction()
    markers = pdf_format.extract_markers(total_wordlst, pdf_rawdata.MARKER_STR)
    valid_lst = pdf_format.extract_words_in_markers(
        total_wordlst,
        markers if markers != None else exit("Markers is empty"),
    )

    print(pdf_format._flatten_lst(valid_lst))

    transactions_lst = pdf_format.sort_to_transactions(valid_lst, markers)
    print(transactions_lst)

    newtransactions_lst = pdf_format.delete_blacklist(transactions_lst)

    pdf_format.pretty_print_transactions(newtransactions_lst)


if __name__ == "__main__":
    # Manual undo/redo check using the sample dataset from config.testin()
    sample_save = core_config.testin()

    with tempfile.TemporaryDirectory() as tmp:
        base = Path(tmp)
        with mock.patch.object(storage, "MAIN_DATA_FILE", base / "storage/save.json"), \
             mock.patch.object(storage, "BACKUP_DIR", base / "storage/backups/"), \
             mock.patch.object(storage, "UNDO_DIR", base / "storage/undo_stack/"), \
             mock.patch.object(storage, "REDO_DIR", base / "storage/redo_stack/"):

            storage.save(sample_save)
            storage.cr_backup_lst(sample_save, mode="undo", delbackup=False)

            updated_save = [dict(txn) for txn in sample_save]
            if updated_save:
                updated_save[0]["amount"] = updated_save[0].get("amount", 0) + 1
            storage.save(updated_save)

            undo_status, undo_data = storage.undo_action()
            redo_status, redo_data = storage.redo_action()

            print("Undo status/data:", undo_status, len(undo_data) if undo_data else None)
            print("Redo status/data:", redo_status, len(redo_data) if redo_data else None)
