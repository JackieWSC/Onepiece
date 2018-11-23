from django.shortcuts import render
from django.http import HttpResponse
from stocksapi.models import StockPriceStatistics, Visitor
from bs4 import BeautifulSoup
import datetime
import pandas
import pandas_datareader as datareader
import re
import requests
import time


log_level = 'debug'


def log_trace(name, log):
    global log_level
    if log_level == 'debug':
        print('Log Level (debug) - Name:' + name)
        print(log)


def get_decimal(stock_code):
    stock_decimal = {
        "2800.HK": 1,
        "^HSI": -2,
    }

    return stock_decimal[stock_code]


def check_stock_code(stock_code):
    if stock_code == "HSI":
        stock_code = "^HSI"
    return stock_code


def check_price_tick(stock_code):
    stock_price_tick = {
        "2800.HK": 0.1,
        "^HSI": 100,
    }

    return stock_price_tick[stock_code]


def check_start_date(year):
    if year == 10:
        start = datetime.datetime(2008, 1, 1)
    elif year == 3:
        start = datetime.datetime(2015, 1, 1)
    elif year == 1:
        start = datetime.datetime(2018, 1, 1)
    else:
        year = 10
    return start, year


def get_stock_name(stock_code):
    stock_code = check_stock_code(stock_code)

    link = "http://d.yimg.com/autoc.finance.yahoo.com/autoc?query={}&region=1&lang=en".format(stock_code)
    result = requests.get(link).json()
    stock_name = ""

    for data in result['ResultSet']['Result']:
        if data['symbol'] == stock_code:
            stock_name = data['name']

    return stock_name


def create_kd_index(stock_code):
    # get the stock data from pandas_datareader
    # stock_code = '2800.HK'
    # start = datetime.datetime(2018, 8, 22)
    stock_code = check_stock_code(stock_code)

    end = datetime.date.today()
    start = datetime.date.today() - datetime.timedelta(days=50)
    stocks_df = datareader.get_data_yahoo(stock_code, start=start, end=end)
    display_trading_day = 20

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
        # print(date.strftime('%Y-%m-%d'))
        # print("Date:{0} RSV:{1:0.4f} K:{2:0.4f} D:{3:0.4f}".format(date, RSV, today_K, today_D))
        date_list.append(date.strftime('%Y-%m-%d'))
        RSV_list.append(format(RSV, '.4f'))
        K_list.append(format(today_K, '.4f'))
        D_list.append(format(today_D, '.4f'))
        ClosePrice_List.append(format(Cn, '.2f'))

    # define each column for the dataframe
    data = {
        'Date': date_list,
        'Close': ClosePrice_List,
        'RSV': RSV_list,
        'K': K_list,
        'D': D_list
    }

    # create define trading day, no need to show all records
    kd_df = pandas.DataFrame(data=data, index=date_list)
    kd_df = kd_df.iloc[-display_trading_day:]

    return kd_df.to_json(orient='records')


def calculate_k(Close, Hn, Ln, previous_K):
    if Close < Ln:
        Ln = Close

    if Close > Hn:
        Hn = Close

    RSV = (Close - Ln) / (Hn - Ln)
    K = ((1 / 3) * RSV) + ((2 / 3) * previous_K)
    #print("Close:{0} K:{1} RSV:{2}".format(Close, K, RSV))

    return K


def notify_line(send, date, close_price, k_value):
    if send:
        close_price = format(close_price, '.2f')
        k_value = format(k_value * 100, '.2f')
        date_str = date.strftime('%Y-%m-%d')

        print('notify line - date:{0}, close_price:{1}, k_value:{2}'.format(
            date_str, close_price, k_value))

        IFTTT_WEBHOOKS_URL = 'https://maker.ifttt.com/trigger/{}/with/key/{}'
        event = 'stockLine'
        token = 'jSfmLiQN7-TxzISuY3kE6p-gusxDr3CTivpaHqNWFCG'

        url_ifttt = IFTTT_WEBHOOKS_URL.format(event, token)
        print(url_ifttt)

        # playload
        data = {
            'value1': date_str,
            'value2': close_price,
            'value3': k_value
        }

        # send the request
        req = requests.post(url_ifttt, data)
        print('The request text:' + req.text)


def create_next_kd_index(stock_code, sned_to_line=False):
    stock_code = check_stock_code(stock_code)

    # get the stock data from pandas_datareader
    # stock_code = '2800.HK'
    # start = datetime.datetime(2018, 8, 22)
    end = datetime.date.today()
    start = datetime.date.today() - datetime.timedelta(days=50)
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
    type_list = []

    # first 1
    k = calculate_k(Cn, Hn, Ln, previous_K)
    Close_List.append(format(Cn, '.2f'))
    Price_List.append(format(Cn, '.2f'))
    K_list.append(format(k, '.4f'))
    type_list.append("START")

    # send the notification to line
    notify_line(sned_to_line, date, Cn, previous_K)

    stock_price_tick = check_price_tick(stock_code)

    # 20 tick for up price
    for i in range(1, 10):
        next_close = Cn + (i * stock_price_tick)
        k = calculate_k(next_close, Hn, Ln, previous_K)

        K_str = format(k, '.4f')
        if K_list[-1] == K_str:
            break

        # print("Close:{0} K:{1}".format(next_close, k))
        Close_List.append(format(Cn, '.2f'))
        Price_List.append(format(next_close, '.2f'))
        K_list.append(format(k, '.4f'))
        type_list.append("UP")


    # 20 tick for down priceß
    for i in range(1, 10):
        next_close = Cn - (i * stock_price_tick)
        k = calculate_k(next_close, Hn, Ln, previous_K)

        K_str = format(k, '.4f')
        if K_list[-1] == K_str:
            break

        # print("Close:{0} K:{1}".format(next_close, k))
        Close_List.append(format(Cn, '.2f'))
        Price_List.append(format(next_close, '.2f'))
        K_list.append(format(k, '.4f'))
        type_list.append("DOWN")



    data = {
            'Close': Close_List,
            'Price': Price_List,
            'K': K_list,
            'Type': type_list
        }

    kd_df = pandas.DataFrame(data=data)
    kd_df.sort_values('Price', inplace=True)

    return kd_df.to_json(orient='records')


def create_stock_price_hsitory(stock_code, year):
    start, year = check_start_date(year)
    end = datetime.date.today()
    stock_code = check_stock_code(stock_code)

    # User pandas_reader.data.DataReader to load the desired data. As simple as that.
    # df = data.get_data_yahoo('2800.hk', start_date, end_date)
    # the early start day is 2007-12-31
    stock_df = datareader.get_data_yahoo(stock_code, start=start, end=end)
    no_of_record = len(stock_df.index)

    print('create_stock_price_hsitory - no_of_record', no_of_record)

    # round the price to 1 decimal
    decimal = get_decimal(stock_code)
    stock_df['price'] = round(stock_df['Close'], decimal)

    # create count column to count the price
    history_df = stock_df.groupby(['price']) \
            .size() \
            .reset_index(name='count') \
            .sort_values(['price'], ascending=True)

    # create different column
    #   percentage: calculate the distribution of the price
    #   stock: the stock code
    #   period: base on this year, 3, 5,10 years records
    #   remark: show the day
    history_df["percentage"] = round((history_df['count'] / no_of_record) * 100, 1)
    history_df['stock'] = stock_code
    history_df['period'] = str(year)
    history_df['remark'] = '{0} to {1}'.format(start.strftime("%Y-%m-%d"), end.strftime("%Y-%m-%d"))
    # print(history_df)

    write_to_db = False
    # write the data to database
    if write_to_db:
        entries = []
        for entry in history_df.T.to_dict().values():
            # print(entry)
            entries.append(StockPriceStatistics(**entry))

        StockPriceStatistics.objects.bulk_create(entries)

    return history_df.to_json(orient='records')


# Main View Page
def stock_kd(request, stock_code="2800.HK"):
    stock_name = get_stock_name(stock_code)
    context = {
        'stock_name': stock_name,
        'stock_code': stock_code
    }

    return render(request, "stock.html", context)


def stock_history(request, stock_code="2800.HK"):
    stock_name = get_stock_name(stock_code)
    context = {
        'stock_name': stock_name,
        'stock_code': stock_code
    }

    return render(request, "stockhistory.html", context)


def playground(request):
    return render(request, "playground.html")


# Line Notification


# Call by IFTTT and send the message to LINE API
def check_next_kd_index(request):
    start_time = time.time()

    # main function
    send_to_line = True
    create_next_kd_index(send_to_line)

    # calculate the latency
    latency_ms = (time.time() - start_time) * 1000
    visitor = Visitor(page='check_next_kd_index', latency=latency_ms)
    visitor.save()

    return render(request, "index.html")

# RESTFUL API interface


# Get the price history by stock code
# It can get the 1, 3 and 10 years data
def get_stock_price_history(request, stock_code="2800.HK", year=10):
    print(stock_code, year)

    start_time = time.time()

    # main function
    json = create_stock_price_hsitory(stock_code, year)

    # calculate the latency
    latency_ms = (time.time() - start_time) * 1000
    visitor = Visitor(page='stock_price_history', latency=latency_ms)
    visitor.save()

    return HttpResponse(json)


# Get the KD index in last 20 trading date
def get_kd_index(request, stock_code="2800.HK"):
    start_time = time.time()

    # main function
    json = create_kd_index(stock_code)

    # calculate the latency
    latency_ms = (time.time() - start_time) * 1000
    visitor = Visitor(page='kd_index', latency=latency_ms)
    visitor.save()

    return HttpResponse(json)


# Get the KD index of next trading date
def get_next_kd_index(request, stock_code="2800.HK"):
    start_time = time.time()

    # main function
    json = create_next_kd_index(stock_code)

    # calculate the latency
    latency_ms = (time.time() - start_time) * 1000
    visitor = Visitor(page='next_kd_index', latency=latency_ms)
    visitor.save()

    return HttpResponse(json)
