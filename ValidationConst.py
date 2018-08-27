# coding:utf-8
from enum import Enum

class ValidateConst(Enum):
    MIN_DISC_SPACE = 2 # 最低ディスク空き容量(GB)
    MAX_TRIAL_COUNT = 10 # 最大試行回数
    MIN_TRIAL_COUNT = 1 # 最低試行回数
    DEFAULT_TRIAL_COUNT = 3 # デフォルト試行回数
