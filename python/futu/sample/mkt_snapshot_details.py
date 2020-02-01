# -*- coding: utf-8 -*-
"""
Get the Market Snapshot and print detail
"""
import futu as ft
import pandas as pd
import datetime
from time import sleep
import math


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


def print_trading_days(api_svr_ip, api_svr_port, stock_list):
    quote_ctx = ft.OpenQuoteContext(host=api_svr_ip, port=api_svr_port)
    print(quote_ctx.get_trading_days(ft.Market.HK, start='2019-10-10', end='2019-10-10'))
    ret_code, ret_data = quote_ctx.get_market_snapshot(stock_list)

    if ret_code == 0:
        for name, values in ret_data.iteritems():
            # if not numpy.isnan(values[0]):
            if isinstance(values, float):
                if not math.isnan(values):
                    print('{}: {}'.format(name, values[0]))
            else:
                print('{}: {}'.format(name, values[0]))
    quote_ctx.close()


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


def get_static_data(ip, port, stock_list):
    quote_ctx = ft.OpenQuoteContext(ip, port)

    start_time = datetime.time(9, 0, 0)
    end_time = datetime.time(16, 0, 0)

    while True:
        if not time_in_range(start_time, end_time, datetime.datetime.now().time()):
            break

        print('--------------------------------------------------------------------')
        print('Current time:{}'.format(datetime.datetime.now().time()))

        # get snapshot data
        ret_code, ret_data = quote_ctx.get_market_snapshot(stock_list)

        print('\nSnapshot Data:')
        if ret_code == 0:
            # for name, values in ret_data.iteritems():
            #     # if not numpy.isnan(values[0]):
            #     if isinstance(values, float):
            #         if not math.isnan(values):
            #             print('{}: {}'.format(name, values[0]))
            #     else:
            #         print('{}: {}'.format(name, values[0]))
            # with pd.option_context('display.max_rows', None, 'display.max_columns',None):  # more options can be specified also
            #     print(ret_data)

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
        print('\nKLine Data:')
        ret, data, page_reg_key = quote_ctx.request_history_kline(
            stock_list,
            start='2019-10-16',
            end='2019-10-16',
            ktype=ft.KLType.K_30M,
            autype=ft.AuType.QFQ,
            fields=[ft.KL_FIELD.DATE_TIME,
                    ft.KL_FIELD.OPEN,
                    ft.KL_FIELD.CLOSE,
                    ft.KL_FIELD.HIGH,
                    ft.KL_FIELD.LOW])

        print('ret:{}'.format(ret))
        if ret_code == 0:
            with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
                print(data)
            print('page_reg_key:{}'.format(page_reg_key))
        else:
            print('ret code:{}'.format(ret_code))
            print('data:{}'.format(ret_data))

        # get the data every 5 minutes
        sleep(300)

    quote_ctx.close()


if __name__ == "__main__":
    ip = '127.0.0.1'
    port = 11111

    stock = 'HK.800000'
    # stock = 'US.AAPL'
    stock_list = [stock, 'HK.02800']
    # print_mkt_snapshot_details(ip, port, stock_list)
    # print_trading_days(ip, port, stock_list)
    # print_k_line(ip, port, stock)
    get_static_data(ip, port, stock)


