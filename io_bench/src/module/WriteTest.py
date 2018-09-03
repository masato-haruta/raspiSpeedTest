# coding:utf-8
from io_bench.exception.CommandResultParseException import CommandResultParseException
from io_bench.src.module.BaseTest import BaseTest
from io_bench.exception.DiskFreeSpaceException import DiskFreeSpaceException
import io_bench.src.model.SpeedTestValidator
import io_bench.src.model.Parser
import io_bench.src.model.ValidationConst
from io_bench.src.util.Utility import SpeedTestUtil


class WriteTest(BaseTest):
    # 書き込み計測
    @staticmethod
    def exec_write_test_if_needed(parsed_options):
        """
        :type: list
        :rtype: csv or json
        """
        if parsed_options.readTestOnly:
            return
        try:
            # コマンド実行可能かをディスク空き容量確認
            io_bench.src.model.SpeedTestValidator.SpeedTestValidator.write_test_disk_space_validate()

            # 指定試行回数dd実行結果リストを取得。
            result_list = BaseTest.exec_tests(SpeedTestUtil.get_write_test_cmd(parsed_options.debug), parsed_options.number)

            # 実行結果から必要部分をパースして取得
            parsed_results, unit = io_bench.src.model.Parser.SpeedTestParser.parse_cmd_results(result_list, io_bench.src.model.ValidationConst.ValidateConst.WRITE_TEST_RESULT_INDEX.value, io_bench.src.model.ValidationConst.ValidateConst.WRITE_TEST_RESULT_UNIT_INDEX.value)

            # 書き込み速度Max, Min, Avr結果を指定フォーマットで返す
            return io_bench.src.model.Parser.SpeedTestParser.parse_result(parsed_results, parsed_options, unit)
        except DiskFreeSpaceException as e:
            raise DiskFreeSpaceException(e)
        except CommandResultParseException as e:
            raise CommandResultParseException(e)
        finally:
            # 1GBのファイルを存在する場合は削除
            SpeedTestUtil().delete_testfile_if_needed()
