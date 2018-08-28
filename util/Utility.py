# coding:utf-8
import shutil
import subprocess
import os

import Parser
import ValidationConst
import Validator
from exception.CommandResultParseException import CommandResultParseException
from exception.DiskFreeSpaceException import DiskFreeSpaceException
from exception.TargetDirectoryNotFoundException import TargetDirectoryNotFoundException

class SpeedTestUtil:
    save_path = "/tmp/raspi_write_test.tmp"  # 書き込み計測時ファイル保存パス

    read_command = "sudo hdparm -t {0} | sed -e '1d' | awk {1}"
    read_command_debug = "echo 21.91 MB/sec"

    write_command = "(time dd if=/dev/zero of={0} ibs=1m obs=1m count=1024) 2>&1 | sed -e '1, 2d' | awk {1}".format(
         save_path, '\'{print $10, $11}\'')
    write_command_debug = "echo 14.45 MB/sec"

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

    # 試行回数取得
    @staticmethod
    def get_trial_count(number):
        if ValidationConst.ValidateConst.MIN_TRIAL_COUNT.value <= number <= ValidationConst.ValidateConst.MAX_TRIAL_COUNT.value:
            return number
        else:
            return ValidationConst.ValidateConst.DEFAULT_TRIAL_COUNT.value

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
            Validator.Validator.read_test_target_validate(parsed_options.target)

            # 指定試行回数hdparmを実行し計測単位取得及び、計測結果リストを取得。
            SpeedTestUtil.read_command = SpeedTestUtil.read_command.format(parsed_options.target, '\'{print $11, $12}\'')

            # debugオプション時はecho結果を渡す
            if parsed_options.debug:
                SpeedTestUtil.read_command = SpeedTestUtil.read_command_debug
            result_list, result_unit = SpeedTestUtil.exec_tests(SpeedTestUtil.read_command, parsed_options.number)

            # 読み込み速度Avr, Max, Min, 試行回数をJsonで返す
            return Parser.SpeedTestParser.parse_result(result_list, parsed_options)
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
            Validator.Validator.write_test_disk_space_validate()

            # debugオプション時はecho結果を渡す
            if parsed_options.debug:
                SpeedTestUtil.write_command = SpeedTestUtil.write_command_debug

            # 指定試行回数ddを実行し結果をリストに格納
            result_list, result_unit = SpeedTestUtil().exec_tests(SpeedTestUtil.write_command, parsed_options.number)

            # 書き込み速度Max, Min, Avr結果をJsonで返す
            return Parser.SpeedTestParser.parse_result(result_list, parsed_options)
        except DiskFreeSpaceException as e:
            raise DiskFreeSpaceException(e)
        except CommandResultParseException as e:
            raise CommandResultParseException(e)
        finally:
            # 1GBのファイルを存在する場合は削除
            SpeedTestUtil().delete_testfile_if_needed()
