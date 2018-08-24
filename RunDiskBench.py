# coding:utf-8
from exception.CommandResultParseException import CommandResultParseException
from util.SpeedTestUtil import SpeedTestUtil
from exception.DiskFreeSpaceException import DiskFreeSpaceException
from exception.TargetDirectoryNotFoundException import TargetDirectoryNotFoundException

if __name__ == '__main__':
    parsedOpts = SpeedTestUtil().parse_options() # コマンドオプション解析(試行回数と対象ディレクトリを受け取る)
    parsedOpts.number = SpeedTestUtil().get_trial_count(parsedOpts.number) # テスト実行回数取得

    try:
        print("ReadTestResult:" + str(SpeedTestUtil().exec_read_test_if_needed(parsedOpts)))
        print("WriteTestResult:" + str(SpeedTestUtil().exec_write_test_if_needed(parsedOpts)))
    except TargetDirectoryNotFoundException as e:
        print(e)
    except DiskFreeSpaceException as e:
        print(e)
    except CommandResultParseException as e:
        print(e)
