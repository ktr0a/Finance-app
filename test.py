import unittest
from unittest import mock

import core.config as config

from cli.cli_hub_modules.calc_hub import calc_loop
import main


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
    def test_run_cli_exits_before_prehub(self):
        with mock.patch("main.start", return_value=0), \
             mock.patch("main.prehub") as prehub_mock, \
             mock.patch("main.hub") as hub_mock, \
             mock.patch("builtins.print"):
            main.run_cli()

        prehub_mock.assert_not_called()
        hub_mock.assert_not_called()

    def test_run_cli_stops_when_prehub_returns_none(self):
        with mock.patch("main.start", return_value=1), \
             mock.patch("main.prehub", return_value=None) as prehub_mock, \
             mock.patch("main.hub") as hub_mock, \
             mock.patch("builtins.print"):
            main.run_cli()

        prehub_mock.assert_called_once_with(1)
        hub_mock.assert_not_called()


if __name__ == "__main__":
    unittest.main()
