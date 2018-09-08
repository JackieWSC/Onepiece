import requests
import json, csv
import matplotlib.pyplot as plt
import pandas as pd
import os
import time

def twodigiit(n):
    if (n<10):
        result = '0' + str(n)
    else:
        result = str(n)

    return result


def convertDateTW(date):
    strl = str(date)
    yearstr = strl[:3]
    realyear = str(int(yearstr) + 1911)
    realdate = realyear + strl[4:6] + strl[7:9]
    return realdate


def convertDateEN(date):
    strl = str(date)
    realdate = strl[:4] + strl[5:7] + strl[8:10]
    return realdate

# main

pd.options.mode.chained_assignment = None
month_file_path = 'stockmonth01.csv'
year_file_path = 'stockyear18.csv'

# http://www.twse.com.tw/exchangeReport/FMSRFK?response=json&date=20180907&stockNo=0050&_=1536332241014
# http://www.twse.com.tw/en/exchangeReport/STOCK_DAY_AVG?response=json&date=20180907&stockNo=0050&_=1536332504163
# http://www.twse.com.tw/en/exchangeReport/STOCK_DAY?response=json&date=20180907&stockNo=0050&_=1536332845660
if not os.path.isfile(month_file_path):
    url_twse = 'http://www.twse.com.tw/en/exchangeReport/STOCK_DAY?response=json&date=20180907&stockNo=0050&_=1536332845660'
    res = requests.get(url_twse)
    jdata = json.loads(res.text)

    outputfile = open(month_file_path, 'w', newline='')
    outputwriter = csv.writer(outputfile)
    outputwriter.writerow(jdata['fields'])
    for dataline in (jdata['data']):
        outputwriter.writerow(dataline)
    outputfile.close()

url_head = "http://www.twse.com.tw/en/exchangeReport/STOCK_DAY?response=json&date=2018"
url_tail = "01&stockNo=0050&_=1536332845660"

if not os.path.isfile(year_file_path):
    # collect the Jan to Sep data
    for i in range(1, 10):
        url_twse = url_head + twodigiit(i) + url_tail
        print(url_twse)
        res = requests.get(url_twse)
        jdata = json.loads(res.text)

        outputfile = open(year_file_path, 'a', newline='')
        outputwriter = csv.writer(outputfile)
        if (i==1):
            outputwriter.writerow(jdata['fields'])

        for dataline in (jdata['data']):
            outputwriter.writerow(dataline)

        time.sleep(1)

    outputfile.close()


# convert to line graph
pdstock = pd.read_csv(year_file_path)
for i in range(len(pdstock['Date'])):
    pdstock['Date'][i] = convertDateEN(pdstock['Date'][i])
pdstock['Date'] = pd.to_datetime(pdstock['Date'])
pdstock.plot(kind='line',
             figsize=(12, 6),
             x='Date',
             y=['Opening Price','Highest Price','Lowest Price'])
plt.show()
