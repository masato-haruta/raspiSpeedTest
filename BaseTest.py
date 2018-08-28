# coding:utf-8
import subprocess

from exception.CommandResultParseException import CommandResultParseException


class BaseTest:
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
            except ValueError:
                raise CommandResultParseException("コマンド実行結果を正しくパースできていません: " + stdout_data.decode())

        return scored_list, unit
