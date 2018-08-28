# coding:utf-8
import shutil
import os

from model import ValidationConst


class SpeedTestUtil:
    save_path = "/tmp/raspi_write_test.tmp"  # 書き込み計測時ファイル保存パス

    read_command = "sudo hdparm -t {0} | sed -e '1d' | awk {1}"
    read_command_debug = "echo 21.91 MB/sec"

    write_command = "(time dd if=/dev/zero of={0} ibs=1m obs=1m count=1024) 2>&1 | sed -e '1, 2d' | awk {1}".format(
        save_path, '\'{print $10, $11}\'')
    write_command_debug = "echo 14.45 MB/sec"

    # ディスクの空き容量をGB単位で返す(int)
    @staticmethod
    def get_free_disk_space_gb():
        """

        :rtype: int
        """
        return int(shutil.disk_usage('./').free / 1024 / 1024 / 1024)

    # 試行回数を返す
    @staticmethod
    def get_trial_count(number):
        """
        :type: int
        :rtype: int
        """
        if ValidationConst.ValidateConst.MIN_TRIAL_COUNT.value <= number <= ValidationConst.ValidateConst.MAX_TRIAL_COUNT.value:
            return number
        else:
            return ValidationConst.ValidateConst.DEFAULT_TRIAL_COUNT.value

    # 書き込み計測用テストファイル削除
    def delete_testfile_if_needed(self):
        if os.path.exists(self.save_path):
            os.remove(self.save_path)  # 1GBのファイルを削除

    # 読み込み実行コマンドを返す
    @staticmethod
    def get_read_test_cmd(parsed_options):
        """
        :type: list
        :rtype: str
        """
        return SpeedTestUtil.read_command_debug if parsed_options.debug else SpeedTestUtil.read_command.format(
            parsed_options.target, '\'{print $11, $12}\'')

    # 書き込み実行コマンドを返す
    @staticmethod
    def get_write_test_cmd(is_debug):
        """
        :type: list
        :rtype: str
        """
        return SpeedTestUtil.write_command_debug if is_debug else SpeedTestUtil.write_command
