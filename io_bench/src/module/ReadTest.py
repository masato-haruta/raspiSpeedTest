# coding:utf-8
from io_bench.src.module.BaseTest import BaseTest
from io_bench.exception.CommandResultParseException import CommandResultParseException
from io_bench.exception.TargetDirectoryNotFoundException import TargetDirectoryNotFoundException
import io_bench.src.model.SpeedTestValidator
import io_bench.src.model.Parser
import io_bench.src.model.ValidationConst
from io_bench.src.util.Utility import SpeedTestUtil


class ReadTest(BaseTest):
    # 読み込み計測
    @staticmethod
    def exec_read_test_if_needed(parsed_options):
        """
        :type: list
        :rtype: csv or json
        """
        if parsed_options.writeTestOnly:
            return
        try:
            # 指定ディレクトリ存在確認
            io_bench.src.model.SpeedTestValidator.SpeedTestValidator.read_test_target_validate(parsed_options.target)

            # 指定試行回数hdparm実行結果リストを取得。
            result_list = BaseTest.exec_tests(SpeedTestUtil.get_read_test_cmd(parsed_options.debug, parsed_options.target),
                                                           parsed_options.number)
            # 実行結果から必要部分をパースして取得
            parsed_results, unit = io_bench.src.model.Parser.SpeedTestParser.parse_cmd_results(result_list, io_bench.src.model.ValidationConst.ValidateConst.READ_TEST_RESULT_INDEX.value, io_bench.src.model.ValidationConst.ValidateConst.READ_TEST_RESULT_UNIT_INDEX.value)

            # 読み込み速度Avr, Max, Min, 試行回数を指定フォーマットで返す
            return io_bench.src.model.Parser.SpeedTestParser.parse_result(parsed_results, parsed_options, unit)
        except TargetDirectoryNotFoundException as e:
            raise TargetDirectoryNotFoundException(e)
        except CommandResultParseException as e:
            raise CommandResultParseException(e)
