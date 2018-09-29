from django.shortcuts import render
from django.http import HttpResponse
import requests
from bs4 import BeautifulSoup
import pandas
import pandas_datareader as datareader
import re
import datetime

log_level = 'debug'

def log_trace(name, log):
    global log_level
    if log_level == 'debug':
        print('Log Level (debug) - Name:' + name)
        print(log)


def days_map(weekdays):
    days = {
        "日": "Sun",
        "－": "Mon",
        "二": "Tue"
    }
    return days.get(weekdays)


# Create your views here.
def createDF(district):
    global df
    year3 = []
    colspans = []
    dates = []
    days = []
    url = 'https://www.cwb.gov.tw/V7/forecast/town368/3Hr/6301000.htm'

    # handle first tr
    today = datetime.datetime.now()
    year3.append("%d" % today.year)
    year3.append("%d" % (today + datetime.timedelta(days=1)).year)
    year3.append("%d" % (today + datetime.timedelta(days=2)).year)

    res = requests.get(url)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'html.parser')
    trs = soup.find_all('tr')
    log_trace('first tr', trs[0])
    tdall = trs[0].findAll('td')
    log_trace('all td in first tr', tdall)

    k = 0
    for i in range(len(tdall)):
        td = tdall[i]
        if i > 0: # skip index 0
            if td.has_attr('colspan'):
                colspans.append(td.attrs['colspan'])
            else:
                colspans.append(1)
            monthdate = re.findall('\d+', td.text)
            log_trace('td text', td.text)
            log_trace('month date', monthdate)

            dates.append(year3[k] + '-' + monthdate[0] + '-' + monthdate[1])
            log_trace('dates', dates)

            days_tw = re.findall('[一|二|三|四|五|六|日]', td.text)
            log_trace('days_tw', days_tw[0])
            days.append(days_map(days_tw[0]))
            log_trace('days', days)

            k += 1


    # handle 2nd tr
    ts = []
    weekdays = []
    hours = trs[1].findAll('span')
    k = 0
    for i in range(0, len(colspans)):
        for j in range(0, int(colspans[i])):
            ts.append(dates[i] + ' ' + hours[k].text)
            k += 1
            weekdays.append(days[i])

    df['DateTime'] = ts
    df['Weekday'] = weekdays


    # handle 3rd tr
    wxs = []
    for img in trs[2].findAll('img'):
        wxs.append(img.attrs['alt'])
    df['Weather'] = wxs

    # handle 4 to 10
    vals = []
    for i in range(3, 10):
        if i is not 8:
            tdall = trs[i].findAll('td')
            for j in range(len(tdall)):
                td = tdall[j]
                if j > 0:
                    vals.append(td.text)

            df.iloc[:,i] = vals
            vals = []

    # handle 9
    pops = []
    rep = 0
    tdall = trs[8].findAll('td')
    for i in range(len(tdall)):
        td = tdall[i]
        if i > 0 :
            if td.has_attr('colspan'):
                rep = int(td.attrs['colspan'])
            else:
                rep = 1

            for j in range(0,rep):
                pops.append(td.text)
    df['RainingPops'] = pops


def create_kd_index():
    global df

    # get the stock data from pandas_datareader
    stock_code = '2800.HK'
    start = datetime.datetime(2018, 8, 22)
    end = datetime.date.today()
    stocks_df = datareader.get_data_yahoo(stock_code, start=start, end=end)

    # temp variable
    num_of_row = len(stocks_df.index)
    previous_K = 0
    previous_D = 0

    # record fields
    date_list = []
    RSV_list = []
    K_list = []
    D_list = []
    ClosePrice_List = []

    # as KDJ requires 9 days data to find out the RSV value first
    for i in range(8, num_of_row):
        end = i + 1
        begin = end - 9
        df_max = stocks_df.iloc[begin:end].max()
        df_min = stocks_df.iloc[begin:end].min()

        # calculate the RSV
        date = stocks_df.index[i]
        Hn = df_max['High']
        Ln = df_min['Low']
        Cn = stocks_df.iloc[i]['Close']
        RSV = (Cn-Ln)/(Hn-Ln)

        # calculate the KD value
        if previous_K != 0:
            today_K = ((1/3) * RSV) + ((2/3) * previous_K)
        else:
            today_K = (1 / 2) * RSV

        if previous_D != 0:
            today_D = ((1/3) * today_K) + ((2/3) * previous_D)
        else:
            today_D = (1 / 2) * today_K

        previous_K = today_K
        previous_D = today_D

        # add to lists
        #print(date.strftime('%Y-%m-%d'))
        #print("Date:{0} RSV:{1:0.4f} K:{2:0.4f} D:{3:0.4f}".format(date, RSV, today_K, today_D))
        date_list.append(date.strftime('%Y-%m-%d'))
        RSV_list.append(format(RSV, '.4f'))
        K_list.append(format(today_K, '.4f'))
        D_list.append(format(today_D, '.4f'))
        ClosePrice_List.append(format(Cn, '.2f'))


    data = {
            'Date': date_list,
            'Close': ClosePrice_List,
            'RSV': RSV_list,
            'K': K_list,
            'D': D_list
        }

    df = pandas.DataFrame(data=data, index=date_list)


def calculate_k(Close, Hn, Ln, previous_K):
    if Close < Ln:
        Ln = Close

    if Close > Hn:
        Hn = Close

    RSV = (Close - Ln) / (Hn - Ln)
    K = ((1 / 3) * RSV) + ((2 / 3) * previous_K)
    #print("Close:{0} K:{1} RSV:{2}".format(Close, K, RSV))

    return K


def create_next_kd_index():
    global df

    # get the stock data from pandas_datareader
    stock_code = '2800.HK'
    start = datetime.datetime(2018, 8, 22)
    end = datetime.date.today()
    stocks_df = datareader.get_data_yahoo(stock_code, start=start, end=end)

    # temp variable
    num_of_row = len(stocks_df.index)
    previous_K = 0
    previous_D = 0

    # as KDJ requires 9 days data to find out the RSV value first
    for i in range(8, num_of_row):
        end = i + 1
        begin = end - 9
        df_max = stocks_df.iloc[begin:end].max()
        df_min = stocks_df.iloc[begin:end].min()

        # calculate the RSV
        date = stocks_df.index[i]
        Hn = df_max['High']
        Ln = df_min['Low']
        Cn = stocks_df.iloc[i]['Close']
        RSV = (Cn-Ln)/(Hn-Ln)

        # calculate the KD value
        if previous_K != 0:
            today_K = ((1/3) * RSV) + ((2/3) * previous_K)
        else:
            today_K = (1 / 2) * RSV

        if previous_D != 0:
            today_D = ((1/3) * today_K) + ((2/3) * previous_D)
        else:
            today_D = (1 / 2) * today_K

        previous_K = today_K
        previous_D = today_D


    # print("High:{0} Low:{1} RSV:{2} Pre K:{3} Pre D:{4}".format(Hn, Ln, RSV, previous_K, previous_D))

    Close_List = []
    Price_List = []
    K_list = []

    # first 1
    k = calculate_k(Cn, Hn, Ln, previous_K)
    Close_List.append(format(Cn, '.2f'))
    Price_List.append(format(Cn, '.4f'))
    K_list.append(format(k, '.4f'))

    # 20 tick
    for i in range(1, 10):
        next_close = Cn + (i * 0.1)
        k = calculate_k(next_close, Hn, Ln, previous_K)

        K_str = format(k, '.4f')
        if K_list[-1] == K_str:
            break

        # print("Close:{0} K:{1}".format(next_close, k))
        Close_List.append(format(Cn, '.2f'))
        Price_List.append(format(next_close, '.2f'))
        K_list.append(format(k, '.4f'))

    # 20 tick
    for i in range(1, 10):
        next_close = Cn - (i * 0.1)
        k = calculate_k(next_close, Hn, Ln, previous_K)

        K_str = format(k, '.4f')
        if K_list[-1] == K_str:
            break

        # print("Close:{0} K:{1}".format(next_close, k))
        Close_List.append(format(Cn, '.2f'))
        Price_List.append(format(next_close, '.2f'))
        K_list.append(format(k, '.4f'))



    data = {
            'Close': Close_List,
            'Price': Price_List,
            'K': K_list
        }

    df = pandas.DataFrame(data=data)
    df.sort_values('Price', inplace=True)


df = ''
def index(request):
    return render(request, "stock.html")


def threeday(request, district=None):
    global df
    columns = ['DateTime',
               'Weekday',
               'Weather',
               'Temperature',
               'Temperature 2',
               'WindLevel',
               'WindDirection',
               'Humidity',
               'RainingPops',
               'Conform']

    df = pandas.DataFrame(columns=columns)
    createDF(district)
    json = df.to_json(orient='records', force_ascii=False)
    return HttpResponse(json)


def kd_index(request):
    global df
    create_kd_index()
    json = df.to_json(orient='records')
    return HttpResponse(json)


def next_kd_index(request):
    global df
    create_next_kd_index()
    json = df.to_json(orient='records')
    return HttpResponse(json)

