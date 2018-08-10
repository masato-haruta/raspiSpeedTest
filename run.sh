#!/bin/sh

PATH=$PATH:/usr/local/bin

cd `dirname $0`
bin/speedtest-csv | python gsheet_add.py
