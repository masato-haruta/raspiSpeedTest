# coding:utf-8
from io_bench.src.module.ReadTest import ReadTest
from io_bench.src.module.WriteTest import WriteTest
from io_bench.src.model import Parser
from io_bench.exception.CommandResultParseException import CommandResultParseException
from io_bench.exception.DiskFreeSpaceException import DiskFreeSpaceException
from io_bench.exception.TargetDirectoryNotFoundException import TargetDirectoryNotFoundException

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
