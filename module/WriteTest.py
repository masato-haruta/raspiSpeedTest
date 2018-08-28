# coding:utf-8
from module.BaseTest import BaseTest
from exception.CommandResultParseException import CommandResultParseException
from exception.DiskFreeSpaceException import DiskFreeSpaceException
import model.SpeedTestValidator
import model.Parser
from util.Utility import SpeedTestUtil


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
            model.SpeedTestValidator.SpeedTestValidator.write_test_disk_space_validate()

            # 指定試行回数ddを実行し結果をリストに格納
            result_list, result_unit = BaseTest.exec_tests(SpeedTestUtil.get_write_test_cmd(parsed_options.debug),
                                                           parsed_options.number)

            # 書き込み速度Max, Min, Avr結果を指定フォーマットで返す
            return model.Parser.SpeedTestParser.parse_result(result_list, parsed_options, result_unit)
        except DiskFreeSpaceException as e:
            raise DiskFreeSpaceException(e)
        except CommandResultParseException as e:
            raise CommandResultParseException(e)
        finally:
            # 1GBのファイルを存在する場合は削除
            SpeedTestUtil().delete_testfile_if_needed()
