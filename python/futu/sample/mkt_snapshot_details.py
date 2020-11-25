# -*- coding: utf-8 -*-
"""
Get the Market Snapshot and print detail
"""
import futu as ft
import pandas as pd
import datetime
from time import sleep
import math


# test the request_history_kline function, get the data to calculate KD
#
# output example:
#           code             time_key      open     close      high       low
#   0  HK.800000  2019-10-16 10:30:00  26553.90  26598.59  26653.19  26432.43
#   1  HK.800000  2019-10-16 11:30:00  26594.26  26524.38  26698.56  26484.05
#   2  HK.800000  2019-10-16 12:00:00  26526.77  26505.95  26565.10  26499.25
#   3  HK.800000  2019-10-16 14:00:00  26505.95  26596.06  26631.73  26505.95
#   4  HK.800000  2019-10-16 15:00:00  26594.36  26646.71  26665.85  26585.28
#   5  HK.800000  2019-10-16 16:00:00  26643.58  26664.28  26694.38  26599.31#
def print_k_line(api_svr_ip, api_svr_port, stock_code):
    quote_ctx = ft.OpenQuoteContext(host=api_svr_ip, port=api_svr_port)

    ret, data, page_reg_key = quote_ctx.request_history_kline(
        stock_code,
        start='2019-10-16',
        end='2019-10-16',
        ktype=ft.KLType.K_60M,
        autype=ft.AuType.QFQ,
        fields=[ft.KL_FIELD.DATE_TIME,
                ft.KL_FIELD.OPEN,
                ft.KL_FIELD.CLOSE,
                ft.KL_FIELD.HIGH,
                ft.KL_FIELD.LOW])

    print('ret:{}'.format(ret))
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
        print(data)
    # print('data:{}'.format(data))
    print('page_reg_key:{}'.format(page_reg_key))

    quote_ctx.close()


# test the get_market_snapshot function, list out all columns in snapshot data
#
# output example:
#   code: HK.800000
#   update_time: 2020-03-03 16:00:00
#   last_price: 26284.82
#   open_price: 26419.13
#   high_price: 26527.75
#   low_price: 26233.39
#   prev_close_price: 26291.68
#   volume: 0
#   turnover: 116492564645.05
#   turnover_rate: 0.0
#   suspension: False
#   listing_date: 1970-01-01
#   lot_size: 0
#   price_spread: 0.01
#   stock_owner: nan
#   ask_price: 0.0
#   bid_price: 0.0
#   ask_vol: 0
#   bid_vol: 0
def print_mkt_snapshot_details(api_svr_ip, api_svr_port, stock_list):
    quote_ctx = ft.OpenQuoteContext(host=api_svr_ip, port=api_svr_port)
    ret_code, ret_data = quote_ctx.get_market_snapshot(stock_list)

    if ret_code == 0:
        for name, values in ret_data.iteritems():
            # if not numpy.isnan(values[0]):
            if isinstance(values, float):
                if not math.isnan(values):
                    print('{}: {}'.format(name, values[0]))
            else:
                print('{}: {}'.format(name, values[0]))

        # for column in ret_data:
        #         print('{}: {}'.format(column, ret_data[column]))
    else:
        print('ret code:{}'.format(ret_code))
        print('data:{}'.format(ret_data))

    quote_ctx.close()


def time_in_range(start_time, end_time, time):
    if start_time <= end_time:
        return start_time <= time <= end_time
    else:
        return start_time <= time or time <= end_time


# base on the stock_list to query the following data
#   get_market_snapshot
#   request_history_kline
def get_static_data(ip, port, stock_list):
    quote_ctx = ft.OpenQuoteContext(ip, port)

    start_time = datetime.time(9, 0, 0)
    end_time = datetime.time(23, 0, 0)

    while True:
        if not time_in_range(start_time, end_time, datetime.datetime.now().time()):
            break

        print('--------------------------------------------------------------------')
        print('Current time:{}'.format(datetime.datetime.now().time()))

        # get snapshot data
        ret_code, ret_data = quote_ctx.get_market_snapshot(stock_list)

        print('\nSnapshot Data:')
        if ret_code == 0:
            for index, row in ret_data.iterrows():
                print('code:{code}, update_time:{update_time}, last_price:{last_price}, open_price:{open_price}'.format(
                    code=row['code'],
                    update_time=row['update_time'],
                    last_price=row['last_price'],
                    open_price=row['open_price']))
        else:
            print('ret code:{}'.format(ret_code))
            print('data:{}'.format(ret_data))

        # get k line data
        for stock in stock_list:
            print('\nKLine Data:{}'.format(stock))
            ret, data, page_reg_key = quote_ctx.request_history_kline(stock,
                                                                      start='2020-03-04',
                                                                      end='2020-03-04',
                                                                      ktype=ft.KLType.K_30M,
                                                                      autype=ft.AuType.QFQ,
                                                                      fields=[ft.KL_FIELD.DATE_TIME,
                                                                              ft.KL_FIELD.OPEN,
                                                                              ft.KL_FIELD.CLOSE,
                                                                              ft.KL_FIELD.HIGH,
                                                                              ft.KL_FIELD.LOW])

            print('Request History KLine ret:{}'.format(ret))
            if ret_code == 0:
                # data['delta'] = data['close'] - data['open']
                print(data)
                print('page_reg_key:{}'.format(page_reg_key))
            else:
                print('ret code:{}'.format(ret_code))
                print('data:{}'.format(ret_data))

        # get the data every 5 minutes
        sleep(300)

    quote_ctx.close()


# use the futu api function to monitor the stocks
#   snapshot data
#     * max 4000 stocks per time
#     * max request 60/30 second
#   k line data
#     * max request 60/30 second
if __name__ == "__main__":
    # gateway setup
    ip = '127.0.0.1'
    port = 11111

    # pandas setup
    pd.set_option('display.max_columns', 100)
    pd.set_option('display.width', 1000)

    # monitor stock list
    #stock = 'HK.800000'
    stock = 'US.AAPL'
    stock_list = [stock, 'HK.02800']

    # print_mkt_snapshot_details(ip, port, stock_list)
    # print_k_line(ip, port, stock)
    get_static_data(ip, port, stock_list)


