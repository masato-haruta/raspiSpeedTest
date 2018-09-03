# coding:utf-8
import json
from argparse import ArgumentParser
from statistics import mean

from exception.CommandResultParseException import CommandResultParseException
from model.ValidationConst import ValidateConst
import util.Utility


class SpeedTestParser:
    # コマンドオプション解析
    @staticmethod
    def parse_options():
        """
        :rtype: object
        """
        usage = 'python RunDiskBench.py [-n] [-t </dev/mmcblk0>] [--help]'
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
        argument_parser.add_argument('-d', '--debug',
                                     action='store_true',
                                     help='debug mode. command replace "echo dd, echo hdparm" result')
        parsed_opts = argument_parser.parse_args()
        parsed_opts.number = util.Utility.SpeedTestUtil.get_trial_count(parsed_opts.number)

        return parsed_opts

    # 測定結果のAvr, Max, Min, 試行回数を指定フォーマットで返す(デフォルトはJson)
    @staticmethod
    def parse_result(result_list, parsed_options, unit):
        """
        :type: list, list, str
        :rtype: json or csv
        """
        parsed_result = {'average': mean(result_list), 'max': max(result_list), 'min': min(result_list), 'unit': unit,
                         'trial_count': len(result_list)}

        # 所定のフォーマットにする
        if parsed_options.csv:
            return ','.join(map(str, list(parsed_result.values())))
        else:
            return json.dumps(parsed_result)

    # Read測定結果から必要な部分を取り出して返す
    @staticmethod
    def parse_read_test_results(cmd_results):
        """
        :type: list
        :rtype: list, str
        """
        parsed_results = []
        for i, cmd_result in  enumerate(cmd_results):
            try:
                tmp_list = cmd_result.split(" ")
                parsed_results.append(float(tmp_list[14]))
                unit = tmp_list[15]
            except CommandResultParseException:
                raise CommandResultParseException("コマンド実行結果を正しくパースできていません: " + cmd_results)
        return parsed_results, unit

    # Write測定結果から必要な部分を取り出して返す
    @staticmethod
    def parse_write_test_results(cmd_results):
        """
        :type: list
        :rtype: list, str
        """
        parsed_results = []
        for i, cmd_result in enumerate(cmd_results):
            try:
                tmp_list = cmd_result.split(" ")
                parsed_results.append(float(tmp_list[9]))
                unit = tmp_list[10]
            except CommandResultParseException:
                raise CommandResultParseException("コマンド実行結果を正しくパースできていません: " + cmd_results)
        return parsed_results, unit
