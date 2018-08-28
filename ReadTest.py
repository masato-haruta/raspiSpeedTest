# coding:utf-8
from BaseTest import BaseTest
from exception.CommandResultParseException import CommandResultParseException
from exception.TargetDirectoryNotFoundException import TargetDirectoryNotFoundException
import model.Validator
import model.Parser
from util.Utility import SpeedTestUtil


class ReadTest(BaseTest):
    # 読み込み計測
    @staticmethod
    def exec_read_test_if_needed(parsed_options):
        if parsed_options.writeTestOnly:
            return
        try:
            # 指定ディレクトリ存在確認
            model.Validator.Validator.read_test_target_validate(parsed_options.target)

            # 指定試行回数hdparmを実行し計測単位取得及び、計測結果リストを取得。
            result_list, result_unit = BaseTest.exec_tests(SpeedTestUtil.get_read_test_cmd(parsed_options), parsed_options.number)

            # 読み込み速度Avr, Max, Min, 試行回数をJsonで返す
            return model.Parser.SpeedTestParser.parse_result(result_list, parsed_options, result_unit)
        except TargetDirectoryNotFoundException as e:
            raise TargetDirectoryNotFoundException(e)
        except CommandResultParseException as e:
            raise CommandResultParseException(e)
