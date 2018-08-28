# coding:utf-8
from model import Parser
from exception.CommandResultParseException import CommandResultParseException
from util.Utility import SpeedTestUtil
from exception.DiskFreeSpaceException import DiskFreeSpaceException
from exception.TargetDirectoryNotFoundException import TargetDirectoryNotFoundException

if __name__ == '__main__':
    parsedOpts = Parser.SpeedTestParser().parse_options() # コマンドオプション解析(試行回数と対象ディレクトリを受け取る)

    try:
        print("ReadTestResult:" + str(SpeedTestUtil().exec_read_test_if_needed(parsedOpts)))
        print("WriteTestResult:" + str(SpeedTestUtil().exec_write_test_if_needed(parsedOpts)))
    except TargetDirectoryNotFoundException as e:
        print(e)
    except DiskFreeSpaceException as e:
        print(e)
    except CommandResultParseException as e:
        print(e)
