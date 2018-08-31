# coding:utf-8
import shutil
import os

from model import ValidationConst


class SpeedTestUtil:
    save_path = "/tmp/raspi_write_test.tmp"  # 書き込み計測時ファイル保存パス

    read_command = "sudo hdparm -t {0} | sed -e '1, 2d'"
    read_command_debug = "echo Timing buffered disk reads:  36 MB in  3.13 seconds =  11.48 MB/sec"

    write_command = "dd if=/dev/zero of={0} ibs=1M obs=1M count=1024 2>&1 | sed -e {1}".format(save_path, "'1, 2d'")
    write_command_debug = "echo '1073741824 bytes (1.1 GB, 1.0 GiB) copied, 88.6369 s, 12.1 MB/s'"

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
    def get_read_test_cmd(is_debug, target):
        """
        :type: list
        :rtype: str
        """
        return SpeedTestUtil.read_command_debug if is_debug else SpeedTestUtil.read_command.format(target)

    # 書き込み実行コマンドを返す
    @staticmethod
    def get_write_test_cmd(is_debug):
        """
        :type: list
        :rtype: str
        """
        return SpeedTestUtil.write_command_debug if is_debug else SpeedTestUtil.write_command
