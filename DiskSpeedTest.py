import subprocess
import shutil
import json
import os.path
from argparse import ArgumentParser


# 空き容量(GB単位)確認。２GB以上が必要
def isOverEmptyDiskSpace():
    emptyDisk_gb = int(shutil.disk_usage('./').free / 1024 / 1024 / 1024)
    if emptyDisk_gb <= 2:
        print("空き容量が不足しているため書き込みテストを実行できません。2GB以上の空きが必要です。")
        exit(1)

# 読み込みテストに指定したディレクトリが存在するか確認
def isExistTarget(target):
    if not os.path.exists(target):
        print("対象のディレクトリまたはファイルが存在しないためテストを実行できません。fdick -l で出力されたものを参考に指定し直してください")
        exit(1)

# コマンドオプション解析
def parseOpts():
    usage = 'python {} [-n] [-t </dev/mmcblk0>] [--help]' \
        .format(__file__)
    argparser = ArgumentParser(usage = usage)
    argparser.add_argument('-n', '--number',
                           action = 'store',
                           type = int,
                           help = 'number of trials. 1 <= number <= 10 default 3.')
    argparser.add_argument('-t', '--target',
                           action='store',
                           type = str,
                           required = True,
                           help = 'read speed test target dir')
    return argparser.parse_args()

# 試行回数取得
def getTestCount(number):
    if 1 <= number <= 10:
        return number
    else:
        return 3

# hdparm実行結果をパースして数値と単位のリストにして返す
def parseResultStr(commandResultStr):
    return commandResultStr.split(" ")

# 指定回数commandを回し、結果をListで返す
def execTests(command, testCount):
    scoredList = [] # 計測結果格納用
    unit = "" # 計測単位

    for i in range(testCount):
        command = "echo 24.02 MB/sec" # デバッグ用
        proc = subprocess.Popen(command, shell = True, stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
        stdoutData, stderrData = proc.communicate()  # 処理実行を待つ
        if len(stderrData) > 0:
            print("{} execute error:".format(command) + stderrData.decode())
            continue

        parsedResultList = parseResultStr(stdoutData.decode())
        unit = parsedResultList[1] # 単位(MB/sec)取得

        scoredList.append(float(parsedResultList[0])) # 値取得しListに追加

    return scoredList, unit

# 測定結果のAvr, Max, MinをJsonで返す
def getSortResultWithJson(resultList):
    parseResultDict = {}
    parseResultDict['average'] = sum(resultList) / len(resultList)
    parseResultDict['max'] = max(resultList)
    parseResultDict['min'] = min(resultList)
    parseResultDict['test_count'] = len(resultList)

    return json.dumps(parseResultDict)

if __name__ == '__main__':
    parsedOpts = parseOpts() # コマンドオプション解析(試行回数と対象ディレクトリを受け取る)
    # 読み込み計測
    # 指定ディレクトリが存在するか確認
    isExistTarget(parsedOpts.target)

    # 指定試行回数hdparmを実行し計測単位取得及び、計測結果リストを取得。
    command = "sudo hdparm -t {0} | awk {1}".format(parsedOpts.target, '{print $10, $11}')
    readResultList, readTestUnit = execTests(command, getTestCount(parsedOpts.number))

    # 読み込み速度Avr, Max, Min, 試行回数をJsonで返す
    jsonReadTestResult = getSortResultWithJson(readResultList)

    # 書き込み計測
    isOverEmptyDiskSpace() # コマンド実行可能かをディスク空き容量確認
    # 指定試行回数ddを実行し結果をリストに格納
    savePath = "/tmp/raspi_write_test.tmp"
    command = "time dd if=/dev/zero of={0} ibs=1M obs=1M count=1024 | awk {1}".format(savePath, '{print $10,  $11}')
    writeResultList, writeTestUnit = execTests(command, getTestCount(parsedOpts.number))
    #os.remove(savePath) # 1GBのファイルを削除

    # 書き込み速度Max, Min, Avr結果をJsonで返す
    jsonWriteTestResult = getSortResultWithJson(writeResultList)

    print(jsonReadTestResult)
    print(jsonWriteTestResult)