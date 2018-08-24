# coding:utf-8
import json
import shutil
from argparse import ArgumentParser
import subprocess
from enum import Enum
from statistics import mean
import os

from exception.CommandResultParseException import CommandResultParseException
from exception.DiskFreeSpaceException import DiskFreeSpaceException
from exception.TargetDirectoryNotFoundException import TargetDirectoryNotFoundException

class ValidateConst(Enum):
    MIN_DISC_SPACE = 2 # 最低ディスク空き容量(GB)
    MAX_TRIAL_COUNT = 10 # 最大試行回数
    MIN_TRIAL_COUNT = 1 # 最低試行回数
    DEFAULT_TRIAL_COUNT = 3 # デフォルト試行回数

class SpeedTestUtil:
    save_path = "/tmp/raspi_write_test.tmp"  # 書き込み計測時ファイル保存パス

    read_command = "sudo hdparm -t {0} | sed -e '1d' | awk {1}"
    #read_command = "echo 21.91 MB/sec"

    write_command = "(time dd if=/dev/zero of={0} ibs=1m obs=1m count=1024) 2>&1 | sed -e '1, 2d' | awk {1}".format(
         save_path, '\'{print $10, $11}\'')
    #write_command = "echo 14.45 MB/sec"

    # 指定回数commandを回し、結果をListで返す
    @staticmethod
    def exec_tests(command, trial_count):
        scored_list = []  # 計測結果格納用
        unit = ""  # 計測単位

        for i in range(trial_count):
            process = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE)
            stdout_data, stderr_data = process.communicate()  # 処理実行を待つ
            if len(stderr_data) > 0:
                print("{} execute error:".format(command) + stderr_data.decode())
                continue

            parsed_result_list = stdout_data.decode().strip().split(" ")
            unit = parsed_result_list[1]  # 単位(MB/sec)取得
            try:
                scored_list.append(float(parsed_result_list[0]))  # 値取得しListに追加
            except ValueError as e:
                raise CommandResultParseException("コマンド実行結果を正しくパースできていません: " + stdout_data.decode())

        return scored_list, unit

    # ディスクの空き容量をGB単位で返す(int)
    @staticmethod
    def get_free_disk_space_gb():
        return int(shutil.disk_usage('./').free / 1024 / 1024 / 1024)

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
        return argument_parser.parse_args()

    # 試行回数取得
    @staticmethod
    def get_trial_count(number):
        if ValidateConst.MIN_TRIAL_COUNT.value <= number <= ValidateConst.MAX_TRIAL_COUNT.value:
            return number
        else:
            return ValidateConst.DEFAULT_TRIAL_COUNT.value

    # 測定結果のAvr, Max, MinをJsonで返す
    @staticmethod
    def parse_json_result(result_list):
        parsed_resul = {}
        parsed_resul['average'] = mean(result_list)
        parsed_resul['max'] = max(result_list)
        parsed_resul['min'] = min(result_list)
        parsed_resul['trial_count'] = len(result_list)

        return json.dumps(parsed_resul)

    # 書き込み計測用テストファイル削除
    def delete_testfile_if_needed(self):
        if os.path.exists(self.save_path):
            os.remove(self.save_path)  # 1GBのファイルを削除

    # 読み込み計測
    @staticmethod
    def exec_read_test_if_needed(parsed_options):
        if parsed_options.writeTestOnly:
            return
        try:
            # 指定ディレクトリ存在確認
            SpeedTestUtil.read_test_target_validate(parsed_options.target)

            # 指定試行回数hdparmを実行し計測単位取得及び、計測結果リストを取得。
            #SpeedTestUtil.read_command = SpeedTestUtil.read_command.format(parsedOpts.target, '\'{print $11, $12}\'')
            result_list, resultUnit = SpeedTestUtil.exec_tests(SpeedTestUtil.read_command, parsed_options.number)

            # 読み込み速度Avr, Max, Min, 試行回数をJsonで返す
            return SpeedTestUtil.parse_json_result(result_list)
        except TargetDirectoryNotFoundException as e:
            raise TargetDirectoryNotFoundException(e)
        except CommandResultParseException as e:
            raise CommandResultParseException(e)

    # 書き込み計測
    @staticmethod
    def exec_write_test_if_needed(parsed_options):
        if parsed_options.readTestOnly:
            return
        try:
            # コマンド実行可能かをディスク空き容量確認
            SpeedTestUtil.write_test_disk_space_validate()

            # 指定試行回数ddを実行し結果をリストに格納
            result_list, result_unit = SpeedTestUtil().exec_tests(SpeedTestUtil.write_command, parsed_options.number)

            # 書き込み速度Max, Min, Avr結果をJsonで返す
            return SpeedTestUtil().parse_json_result(result_list)
        except DiskFreeSpaceException as e:
            raise DiskFreeSpaceException(e)
        except CommandResultParseException as e:
            raise CommandResultParseException(e)
        finally:
            # 1GBのファイルを存在する場合は削除
            SpeedTestUtil().delete_testfile_if_needed()

    # 読み込みテスト用指定ディレクトリ存在確認
    @staticmethod
    def read_test_target_validate(target):
        if not os.path.exists(target):
            raise TargetDirectoryNotFoundException("対象のディレクトリまたはファイルが存在しないためテストを実行できません。fdick -l で出力されたものを参考に指定し直してください")

    # 空き容量確認
    @staticmethod
    def write_test_disk_space_validate():
        if SpeedTestUtil.get_free_disk_space_gb() <= ValidateConst.MIN_DISC_SPACE.value:
            raise DiskFreeSpaceException("空き容量が不足しているため書き込みテストを実行できません。2GB以上の空きが必要です。")

if __name__ == '__main__':
    pass
