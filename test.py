import unittest
from unittest import mock

import core.config as config

from cli.cli_hub_modules.calc_hub import calc_loop
import main
import core.storage as storage
import time


class CalcHubTests(unittest.TestCase):
    def setUp(self):
        self.sample_save = config.testin()

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


if __name__ == "__main__":
    save = config.testin()

    
