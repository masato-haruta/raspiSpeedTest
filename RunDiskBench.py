# coding:utf-8
from ReadTest import ReadTest
from WriteTest import WriteTest
from model import Parser
from exception.CommandResultParseException import CommandResultParseException
from exception.DiskFreeSpaceException import DiskFreeSpaceException
from exception.TargetDirectoryNotFoundException import TargetDirectoryNotFoundException

if __name__ == '__main__':
    parsedOpts = Parser.SpeedTestParser().parse_options()  # コマンドオプション解析

    try:
        print("ReadTestResult:" + str(ReadTest().exec_read_test_if_needed(parsedOpts)))
        print("WriteTestResult:" + str(WriteTest().exec_write_test_if_needed(parsedOpts)))
    except TargetDirectoryNotFoundException as e:
        print(e)
    except DiskFreeSpaceException as e:
        print(e)
    except CommandResultParseException as e:
        print(e)
