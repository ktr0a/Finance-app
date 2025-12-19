from __future__ import annotations

from datetime import datetime
from typing import Callable

from finance_app.core.services.summary_config import SummaryConfig


class SummaryService:
    def __init__(self, config: SummaryConfig) -> None:
        self.config = config
        self.calc_functions = {
            label: func
            for (label, _), func in zip(self.config.calc_config, self._calc_sequence())
        }
        self.calc_util_func = [
            (label, self.calc_functions[label], mode)
            for label, mode in self.config.calc_config
        ]
        self.sort_util_func = [
            (self.config.filter_by_key_value_label, self.filter_save),
        ]
        self.sum_util_func = [
            (self.config.summary_options[0], self.summary_alltime),
            (self.config.summary_options[1], self.summary_general_overview),
            (self.config.summary_options[2], self.summary_income_expense_overview),
            (self.config.summary_options[3], self.sum_by_key_value_pair),
            (self.config.summary_options[4], self.sum_by_key_value_pair),
            (self.config.summary_options[5], self.sum_by_key_value_pair),
            (self.config.summary_options[6], self.summary_by_daterange),
            (self.config.summary_options[7], self.summary_by_daterange),
        ]

    def _calc_sequence(self) -> list[Callable[[list], float]]:
        return [
            self.toti_raw,
            self.tote_raw,
            self.netbal_raw,
            self.count_transactions,
            self.avg_transaction_amount,
            self.max_transaction_amount,
            self.min_transaction_amount,
        ]

    def format_value(self, value, mode: str) -> str:
        if mode == self.config.money_format_mode:
            return f"{value:.2f}{self.config.currency_symbol}"
        if mode == self.config.int_format_mode:
            return str(value)
        return str(value)

    def split_ie(self, transactions):
        income = []
        expense = []
        for tx in transactions:
            if tx.get("type") == "I":
                income.append(tx)
            elif tx.get("type") == "E":
                expense.append(tx)
            else:
                raise ValueError(
                    self.config.invalid_transaction_type.format(
                        name=tx.get("name"),
                        type=tx.get("type"),
                    )
                )
        return income, expense

    def toti_raw(self, save) -> float:
        income, _ = self.split_ie(save)
        return sum(t["amount"] for t in income)

    def tote_raw(self, save) -> float:
        _, expense = self.split_ie(save)
        return sum(t["amount"] for t in expense)

    def netbal_raw(self, save) -> float:
        return self.toti_raw(save) - self.tote_raw(save)

    def count_transactions(self, save) -> int:
        return len(save)

    def avg_transaction_amount(self, save) -> float:
        if not save:
            return 0.0
        return sum(v["amount"] for v in save) / len(save)

    def max_transaction_amount(self, save) -> float:
        if not save:
            return 0.0
        return max(v["amount"] for v in save)

    def min_transaction_amount(self, save) -> float:
        if not save:
            return 0.0
        return min(v["amount"] for v in save)

    def filter_save(self, filterby_key, filterby_value, old_save) -> list:
        filtered_save = []

        for item in old_save:
            if filterby_key not in item:
                continue

            item_value = item[filterby_key]

            if isinstance(item_value, str) and isinstance(filterby_value, str):
                if item_value.lower() == filterby_value.lower():
                    filtered_save.append(item)
            else:
                if item_value == filterby_value:
                    filtered_save.append(item)

        return filtered_save

    def _safe_net_balance(self, dataset):
        cleaned = [t for t in dataset if t.get("type") in ("I", "E")]
        if not cleaned:
            return 0.0
        return self.calc_util_func[2][1](cleaned)

    def _apply_calcs(self, summary, dataset):
        for label, func, _ in self.calc_util_func:
            if label not in self.config.required_calcs:
                continue
            result = func(dataset)
            mapped_key = self.config.summary_key_map.get(label, label)
            summary[mapped_key] = result
        return summary

    def initvars(self):
        return self.config.summary_template.copy()

    def summary_alltime(self, filterby_key, filterby_value, save):
        summary = self.initvars()
        summary[self.config.key_value_pair_label] = self.config.summary_options[0]
        return self._apply_calcs(summary, save)

    def summary_general_overview(self, filterby_key, filterby_value, save):
        summary = {}
        summary["Special1"] = self.config.category_overview_title
        summary[self.config.transactions_analyzed_key] = len(save)

        total_categories = list(set(item["category"] for item in save))
        summary["Total Categories"] = len(total_categories)

        category_list = []

        for category in total_categories:
            _, func = self.sort_util_func[0]
            percategory_dict = {}

            filtered_save = func("category", category, save)
            percategory_dict["category_name"] = category
            percategory_dict["count"] = self.calc_util_func[3][1](filtered_save)
            percategory_dict["total"] = self.calc_util_func[2][1](filtered_save)
            category_list.append(percategory_dict)

        category_list.sort(key=lambda cat: cat["total"], reverse=True)

        summary["Categories"] = category_list
        summary[self.config.net_balance_label] = self._safe_net_balance(save)

        return summary

    def summary_income_expense_overview(self, filterby_key, filterby_value, save):
        summary = {}
        summary["Special2"] = self.config.income_expense_overview_title
        summary[self.config.transactions_analyzed_key] = len(save)

        total_types = ["I", "E"]

        for t in total_types:
            _, func = self.sort_util_func[0]
            percategory_dict = {}

            filtered_save = func("type", t, save)
            percategory_dict["count"] = len(filtered_save)
            percategory_dict["total"] = self._safe_net_balance(filtered_save)

            if t == "I":
                summary[self.config.income_label] = percategory_dict
            else:
                summary[self.config.expense_label] = percategory_dict

        summary[self.config.net_balance_label] = self._safe_net_balance(save)

        return summary

    def sum_by_key_value_pair(self, filterby_key, filterby_value, save):
        summary = self.initvars()
        _, func = self.sort_util_func[0]
        filtered_save = func(filterby_key, filterby_value, save)
        summary[self.config.key_value_pair_label] = f"{filterby_key}: {filterby_value}"
        return self._apply_calcs(summary, filtered_save)

    def summary_by_daterange(self, filterby_key, filterby_value, save):
        summary = self.initvars()
        start_date_str, end_date_str = filterby_value
        start_date = datetime.strptime(start_date_str, self.config.date_format)
        end_date = datetime.strptime(end_date_str, self.config.date_format)

        filtered_save = []
        for transaction in save:
            transaction_date = datetime.strptime(transaction["date"], self.config.date_format)
            if start_date <= transaction_date <= end_date:
                filtered_save.append(transaction)

        summary[self.config.key_value_pair_label] = f"From {start_date_str} to {end_date_str}"
        return self._apply_calcs(summary, filtered_save)

    def summary(self, *args, **kwargs):
        summary_func = kwargs.pop("summary_func", None) or kwargs.pop("func", None)
        if summary_func is None:
            option = kwargs.pop("option", None)
            index = kwargs.pop("index", None)
            if option is not None:
                for label, func in self.sum_util_func:
                    if label == option:
                        summary_func = func
                        break
            elif index is not None:
                summary_func = self.sum_util_func[index][1]

        if summary_func is None:
            raise NotImplementedError("Phase 1: not wired yet")

        return summary_func(*args, **kwargs)

    def calc_menu(self):
        return [(label, None, mode) for (label, _func, mode) in self.calc_util_func]

    def run_calc(self, choice: int, transactions):
        label, func, mode = self.calc_util_func[choice - 1]
        result = func(transactions)
        output = self.format_value(result, mode)
        if "expense" in label.lower() and not output.startswith("-"):
            output = f"-{output}"
        return f"{label}: {output}"

    def summary_menu(self):
        return [(label, None) for (label, _func) in self.sum_util_func]

    def summary_template(self):
        return self.config.summary_template
