# coding:utf-8
import json
from argparse import ArgumentParser
from statistics import mean

from ValidationConst import ValidateConst
import util.SpeedTestUtil


class SpeedTestParser:
    # コマンドオプション解析
    @staticmethod
    def parse_options():
        usage = 'python {} [-n] [-t </dev/mmcblk0>] [--help]' \
            .format(__file__)
        argument_parser = ArgumentParser(usage=usage)
        argument_parser.add_argument('-n', '--number',
                                     type=int,
                                     help='number of trials. {0} <= number <= {1} default {2}.'.format(
                                   ValidateConst.MIN_TRIAL_COUNT.value, ValidateConst.MAX_TRIAL_COUNT.value,
                                   ValidateConst.DEFAULT_TRIAL_COUNT.value))
        argument_parser.add_argument('-t', '--target',
                               type=str,
                               required=True,
                               help='read speed test target dir')
        argument_parser.add_argument('-r', '--readTestOnly',
                               action='store_true',
                               help='read only the test to be executed')
        argument_parser.add_argument('-w', '--writeTestOnly',
                               action='store_true',
                               help='write only the test to be executed')
        argument_parser.add_argument('--csv', '--csv',
                               action='store_true',
                               help='test result output, in CSV format')
        argument_parser.add_argument('--json', '--json',
                               action='store_true',
                               help='default test result output, in JSON format')
        parsed_opts = argument_parser.parse_args()
        parsed_opts.number = util.SpeedTestUtil.SpeedTestUtil.get_trial_count(parsed_opts.number)

        return parsed_opts

    # 測定結果のAvr, Max, Min, 試行回数を指定フォーマットで返す(デフォルトはJson)
    @staticmethod
    def parse_result(result_list, parsed_options):
        parsed_result = {}
        parsed_result['average'] = mean(result_list)
        parsed_result['max'] = max(result_list)
        parsed_result['min'] = min(result_list)
        parsed_result['trial_count'] = len(result_list)

        # 所定のフォーマットにする
        if parsed_options.csv:
            return ','.join(map(str, list(parsed_result.values())))
        else:
            return json.dumps(parsed_result)
