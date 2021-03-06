# coding:utf-8
import os

from io_bench.src.model.ValidationConst import ValidateConst
from io_bench.exception.DiskFreeSpaceException import DiskFreeSpaceException
from io_bench.exception.TargetDirectoryNotFoundException import TargetDirectoryNotFoundException
import io_bench.src.util.Utility


class SpeedTestValidator:
    # 読み込みテスト用指定ディレクトリ存在確認
    @staticmethod
    def read_test_target_validate(target):
        if not os.path.exists(target):
            raise TargetDirectoryNotFoundException("対象のディレクトリまたはファイルが存在しないためテストを実行できません。fdick -l で出力されたものを参考に指定し直してください")

    # 空き容量確認
    @staticmethod
    def write_test_disk_space_validate():
        if io_bench.src.util.Utility.SpeedTestUtil.get_free_disk_space_gb() <= ValidateConst.MIN_DISC_SPACE.value:
            raise DiskFreeSpaceException("空き容量が不足しているため書き込みテストを実行できません。2GB以上の空きが必要です。")
