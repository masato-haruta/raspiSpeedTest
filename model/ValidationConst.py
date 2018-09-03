# coding:utf-8
from enum import Enum

class ValidateConst(Enum):
    MIN_DISC_SPACE = 2 # 最低ディスク空き容量(GB)
    MAX_TRIAL_COUNT = 10 # 最大試行回数
    MIN_TRIAL_COUNT = 1 # 最低試行回数
    DEFAULT_TRIAL_COUNT = 3 # デフォルト試行回数
    WRITE_TEST_RESULT_INDEX = 9 # WriteTest数値結果格納Index
    WRITE_TEST_RESULT_UNIT_INDEX = 10 # WriteTest単位結果格納Index
    READ_TEST_RESULT_INDEX = 14 # ReadTest数値結果格納Index
    READ_TEST_RESULT_UNIT_INDEX = 15 # ReadTest単位格納Index