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


def create_kd_index():
    global df

    # get the stock data from pandas_datareader
    stock_code = '2800.HK'
    # start = datetime.datetime(2018, 8, 22)
    end = datetime.date.today()
    start = datetime.date.today() - datetime.timedelta(days=50)
    stocks_df = datareader.get_data_yahoo(stock_code, start=start, end=end)
    dispolay_trading_day = 20

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
    df = pandas.DataFrame(data=data, index=date_list)
    df = df.iloc[-dispolay_trading_day:]


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
    type_list = []

    # first 1
    k = calculate_k(Cn, Hn, Ln, previous_K)
    Close_List.append(format(Cn, '.2f'))
    Price_List.append(format(Cn, '.2f'))
    K_list.append(format(k, '.4f'))
    type_list.append("START")

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
        type_list.append("UP")

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
        type_list.append("DOWN")



    data = {
            'Close': Close_List,
            'Price': Price_List,
            'K': K_list,
            'Type': type_list
        }

    df = pandas.DataFrame(data=data)
    df.sort_values('Price', inplace=True)


def create_stock_price_hsitory(year):
    start = datetime.datetime(2008, 1, 1)
    if year == 10:
        start = datetime.datetime(2008, 1, 1)
    elif year == 3:
        start = datetime.datetime(2015, 1, 1)
    elif year == 1:
        start = datetime.datetime(2018, 1, 1)
    else:
        year = 10

    end = datetime.date.today()
    stock_code = '2800.HK'
    write_to_db = False

    # User pandas_reader.data.DataReader to load the desired data. As simple as that.
    # df = data.get_data_yahoo('2800.hk', start_date, end_date)
    # the early start day is 2007-12-31
    stock_df = datareader.get_data_yahoo(stock_code, start=start, end=end)
    no_of_record = len(stock_df.index)

    # round the price to 1 decimal
    stock_df['price'] = round(stock_df['Close'],1)

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
    history_df['stock'] = '2800.HK'
    history_df['period'] = str(year)
    history_df['remark'] = '{0} to {1}'.format(start.strftime("%Y-%m-%d"), end.strftime("%Y-%m-%d"))
    # print(history_df)

    # write the data to database
    if write_to_db:
        entries = []
        for entry in history_df.T.to_dict().values():
            # print(entry)
            entries.append(StockPriceStatistics(**entry))

        StockPriceStatistics.objects.bulk_create(entries)

    return history_df.to_json(orient='records')


df = ''


def index(request):
    return render(request, "stock.html")


def stock_history(request):
    return render(request, "stockhistory.html")


def get_stock_price_history(request, year=10):
    start_time = time.time()
    print(year)

    # main function
    json = create_stock_price_hsitory(year)

    # calculate the latency
    latency_ms = (time.time() - start_time) * 1000
    visitor = Visitor(page='stock_price_history', latency=latency_ms)
    visitor.save()

    return HttpResponse(json)


def get_kd_index(request):
    global df
    start_time = time.time()

    # main function
    create_kd_index()
    json = df.to_json(orient='records')

    # calculate the latency
    latency_ms = (time.time() - start_time) * 1000
    visitor = Visitor(page='kd_index', latency=latency_ms)
    visitor.save()

    return HttpResponse(json)


def get_next_kd_index(request):
    global df
    start_time = time.time()

    # main function
    create_next_kd_index()
    json = df.to_json(orient='records')

    # calculate the latency
    latency_ms = (time.time() - start_time) * 1000
    visitor = Visitor(page='next_kd_index', latency=latency_ms)
    visitor.save()

    return HttpResponse(json)

