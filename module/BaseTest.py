# coding:utf-8
import subprocess

from exception.CommandResultParseException import CommandResultParseException


class BaseTest:
    # 指定回数commandを実行し、結果をListと計測単位で返す
    @staticmethod
    def exec_tests(command, trial_count):
        """
        :type: str, int
        :rtype: list, str
        """
        cmd_result_list = []  # 計測結果格納用
        unit = ""  # 計測単位

        for i in range(trial_count):
            process = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE)
            stdout_data, stderr_data = process.communicate()  # 処理実行を待つ
            if len(stderr_data) > 0:
                print("{} execute error:".format(command) + stderr_data.decode())
                continue
            cmd_result_list.append(stdout_data.decode())  # 値取得しListに追加
        return cmd_result_list
