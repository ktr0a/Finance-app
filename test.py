import cli.cli as cli
import cli.helper as h
import cli.prettyprint as pp
import cli.prompts as pr

import core.config as config
from core.calc_utils import calc_util_func as c_util
from core.calc_utils import format
from core.sort_utils import sort_util_func as s_util
from core.sum_utils import sum_util_func as sum_util

import core.storage as s


if __name__ == "__main__":
    save = config.testin()
    print(cli.summary_hub(save))
