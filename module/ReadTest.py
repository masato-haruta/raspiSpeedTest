# coding:utf-8
from module.BaseTest import BaseTest
from exception.CommandResultParseException import CommandResultParseException
from exception.TargetDirectoryNotFoundException import TargetDirectoryNotFoundException
import model.SpeedTestValidator
import model.Parser
import model.ValidationConst
from util.Utility import SpeedTestUtil


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
            model.SpeedTestValidator.SpeedTestValidator.read_test_target_validate(parsed_options.target)

            # 指定試行回数hdparm実行結果リストを取得。
            result_list = BaseTest.exec_tests(SpeedTestUtil.get_read_test_cmd(parsed_options.debug, parsed_options.target),
                                                           parsed_options.number)
            # 実行結果から必要部分をパースして取得
            parsed_results, unit = model.Parser.SpeedTestParser.parse_cmd_results(result_list, model.ValidationConst.ValidateConst.READ_TEST_RESULT_INDEX.value, model.ValidationConst.ValidateConst.READ_TEST_RESULT_UNIT_INDEX.value)

            # 読み込み速度Avr, Max, Min, 試行回数を指定フォーマットで返す
            return model.Parser.SpeedTestParser.parse_result(parsed_results, parsed_options, unit)
        except TargetDirectoryNotFoundException as e:
            raise TargetDirectoryNotFoundException(e)
        except ValueError as e:
            raise CommandResultParseException(e)
        except IndexError as e:
            raise CommandResultParseException(e)