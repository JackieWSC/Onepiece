#!/usr/bin/python
import datetime
import futu as ft
import math
import pandas as pd
# from datetime import datetime
from kd_index import KDIndex
from time import sleep
from utilities import Logger, get_line_number


def time_in_range(start_time, end_time, time):
    if start_time <= end_time:
        return start_time <= time <= end_time
    else:
        return start_time <= time or time <= end_time


def get_stock_data(host, port, stock, start_date, end_date):
    # connect to futu api
    quote_ctx = ft.OpenQuoteContext(host, port)

    ret_code, data_frame, page_req_key = quote_ctx.request_history_kline(stock,
                                                                         start_date,
                                                                         end_date,
                                                                         ktype=ft.KLType.K_DAY,
                                                                         autype=ft.AuType.NONE,
                                                                         fields=[ft.KL_FIELD.DATE_TIME,
                                                                                 ft.KL_FIELD.OPEN,
                                                                                 ft.KL_FIELD.CLOSE,
                                                                                 ft.KL_FIELD.HIGH,
                                                                                 ft.KL_FIELD.LOW],
                                                                         max_count=3000)
    print('Result:{}'.format(ret_code))
    print('Key:{}'.format(page_req_key))
    print('Data:\n{}', data_frame)

    sleep(1)
    # disconnect to futu api
    quote_ctx.close()

    return ret_code, data_frame


def get_snapshot_data(host, port, stock):
    # connect to futu api
    quote_ctx = ft.OpenQuoteContext(host, port)

    # get snapshot data
    ret_code, ret_data = quote_ctx.get_market_snapshot(stock)

    # if ret_code == 0:
    #     for name, values in ret_data.iteritems():
    #         # if not numpy.isnan(values[0]):
    #         if isinstance(values, float):
    #             if not math.isnan(values):
    #                 print('{}: {}'.format(name, values[0]))
    #         else:
    #             print('{}: {}'.format(name, values[0]))
    #
    #     # for column in ret_data:
    #     #         print('{}: {}'.format(column, ret_data[column]))
    # else:
    #     print('ret code:{}'.format(ret_code))
    #     print('data:{}'.format(ret_data))

    sleep(1)
    # disconnect to futu api
    quote_ctx.close()

    return ret_code, ret_data


def get_market_data(host,
                    port,
                    stock,
                    buy_in_k_value,
                    sell_out_k_value,
                    data_frame):
    helper = KDIndex()

    reference_data = {
        'date': [],
        'high': [],
        'low': [],
        'close': [],
        'highest': [],
        'lowest': [],
        'rsv': [],
        'k': [],
        'd': []
    }

    reference_data = helper.calculate_kd_with_data(data_frame, reference_data)

    # convert to data frame
    kd_df = pd.DataFrame(data=reference_data, index=reference_data['date'])
    Logger.log_trace('L1', 'trade_report', get_line_number(), kd_df)

    # base paramter
    base_account = 100000  # init value in acc
    sum_account = 100000  # money in acc
    sum_stoke = 0  # total lots
    sum_value = 0  # total value
    sum_gain_loss_rate = 0  # net profile
    sum_fee = 0  # total fee
    trade_type = 0  # type of type

    chicang_rate = 0  # position net profile
    chicang_stoke_avg_cost = 0  # stock cost

    last_price = 0  # stock price at the end date

    dingtou_base = 100000  # money used for each time
    buy_count = 0
    sell_count = 0

    start_time = datetime.time(9, 0, 0)
    end_time = datetime.time(23, 0, 0)
    today = datetime.date.today().strftime('%Y-%m-%d')

    while True:
        if not time_in_range(start_time, end_time, datetime.datetime.now().time()):
            break

        ret_code, current_data = get_snapshot_data(host=host,
                                                   port=port,
                                                   stock=stock)

        # check the K and d with current price
        update_time = current_data.iloc[0]['update_time']
        current_price = current_data.iloc[0]['last_price']

        k, d = helper.check_new_kd_with_price(kd_df, current_price)

        # ETF price
        ret_code, current_data = get_snapshot_data(host=host,
                                                   port=port,
                                                   stock='HK.02800')

        last_price = float(current_data.iloc[0]['last_price'])


        # when buy
        sell_signal = k > sell_out_k_value

        # when sell
        buy_signal = k < buy_in_k_value

        text = ""

        if buy_signal is True:
            text = "BUY"

        if sell_signal is True:
            text = "SELL"

        log = '{0} ${1} (K:{2:0.2f},D:{3:0.2f}) {4} {5} {6}'.format(
            update_time, last_price, k*100, d*100, buy_signal, sell_signal, text)
        Logger.log_trace('L1', 'kd_strategy_simulator', get_line_number(), log)

        stoke = 0
        one_stoke_price = last_price * 1000
        one_unit_stoke = int(dingtou_base / one_stoke_price)

        start_chicang_stoke_avg_cost = chicang_stoke_avg_cost
        start_chicang_rate = 0

        if (chicang_stoke_avg_cost == 0):
            start_chicang_rate = 0
        else:
            start_chicang_rate = ((last_price - chicang_stoke_avg_cost) / chicang_stoke_avg_cost)

        if buy_signal and sum_stoke == 0:
            buy_count += 1
            stoke = one_unit_stoke
            trade_type = "K ({}) value reach, Buy One Unit".format(buy_in_k_value)

            chicang_stoke_avg_cost = ((sum_stoke * chicang_stoke_avg_cost) + (stoke * last_price)) / (
                                       sum_stoke + stoke)

            chicang_rate = (last_price - chicang_stoke_avg_cost) / chicang_stoke_avg_cost

        elif sell_signal and sum_stoke > 0:
            sell_count += 1
            stoke = sum_stoke * -1
            trade_type = "K ({}) value reach, Sell One Unit".format(sell_out_k_value)

            chicang_stoke_avg_cost = 0
            chicang_rate = 0

        if stoke == 0:

            sleep(300)

            # ret_code, kline_data = get_stock_data(host=host,
            #                                       port=port,
            #                                       stock=stock,
            #                                       start_date=today,
            #                                       end_date=today)
            #
            # if ret_code == ft.RET_OK:
            #     kd_df = helper.append_new_data_to_datafrme(kd_df, kline_data)

            continue

        sum_stoke += stoke
        sum_fee += 15
        sum_account -= ((stoke * one_stoke_price) + 15)
        sum_value = sum_account + (sum_stoke * one_stoke_price)
        sum_gain_loss_rate = ((sum_value - base_account) / base_account) * 100

        trade_report = '''
---- {timeKey} --{tradeType}--{oneUnitStoke} (Stoke) ----
  *** Pre Trade Summary ***
      Last Price: ${lastPrice}
      Pre Trade Stoke Average Price: ${startChicangStokeAvgCost}
      Pre Trade Position Gain/Loss Rate: {startChicangRate}%
  *** Trading Day Summary ***
      Trade Stoke: {stoke}
      Last Stoke Average Price: ${chicangStokeAvgCost}
      Last Position Gain/Loss Rate: {chicangRate}%
  *** Clearing Day Summary ***
      Total Stoke: {totalStoke} Stoke (${totalChicangCost})
      Total Cache: ${sumAccount}
      Total Value: ${sumValue}
      Gain/Loss Value: ${gainLostValue}
      Gain/Loss Rate: {gainLostRate}%
      Total Transaction Fee: ${sumFee}
    '''.format(timeKey=update_time,
               tradeType=trade_type,
               oneUnitStoke=one_unit_stoke,
               startChicangStokeAvgCost=format(start_chicang_stoke_avg_cost, '.2f'),
               lastPrice=last_price,
               startChicangRate=format((start_chicang_rate*100), '.2f'),
               stoke=stoke,
               chicangStokeAvgCost=format(chicang_stoke_avg_cost, '.2f'),
               chicangRate=format((chicang_rate*100), '.2f'),
               totalStoke=sum_stoke,
               totalChicangCost=(sum_stoke * chicang_stoke_avg_cost * 1000),
               sumAccount=sum_account,
               sumValue=sum_value,
               gainLostValue=(sum_value-base_account),
               gainLostRate=format(sum_gain_loss_rate, '0.2f'),
               sumFee=sum_fee)

        Logger.log_trace('L1', 'trade_report', get_line_number(), trade_report)

    summary_report = '''
---- Summary Report ----
  *** Buy Sell Summary ***
      Buy: {buyCount}
      Sell: {sellCount}
      Buy Indicator: {buyIndicator}
      Sell Indicator: {sellIndicator}
  *** Clearing Summary ***
      Total Stoke: {totalStoke} Stoke (${totalChicangCost})
      Total Cache: ${sumAccount}
      Total Value: ${sumValue}
      Gain/Loss Value: ${gainLostValue}
      Gain/Loss Rate: {gainLostRate}%
      Total Transaction Fee: ${sumFee}
'''.format(
        buyCount=buy_count,
        sellCount=sell_count,
        buyIndicator=buy_in_k_value,
        sellIndicator=sell_out_k_value,
        totalStoke=sum_stoke,
        totalChicangCost=(sum_stoke * chicang_stoke_avg_cost * 1000),
        sumAccount=sum_account,
        sumValue=sum_value,
        gainLostValue=(sum_value - base_account),
        gainLostRate=format(sum_gain_loss_rate, '0.2f'),
        sumFee=sum_fee)

    Logger.log_trace('Info', 'summary_report', get_line_number(), summary_report)

    return sum_gain_loss_rate


# version 0.1
#
# Init
#   - Create the dataframe with KD index by data, hour
# Get Market Data
#   - Get the current price from snapshot data
# Check the data
#   - check the current price with KD index dataframe
# Place the order if the buy/sell indicator is on4561`1
#   - call the futu api to place the order\

if __name__ == "__main__":
    # Connect to futu api

    pd.set_option('display.max_columns', 100)
    pd.set_option('display.width', 1000)
    Logger.set_log_level('Info L1 Warning')

    # Initial the dataframe with KD index
    stock = 'HK.800000'
    # stock = 'HK.02800'
    ret_code, ret_data = get_stock_data(host='127.0.0.1',
                                        port=11111,
                                        stock=stock,
                                        start_date='2020-01-02',
                                        end_date='2020-03-08')
    if ret_code == ft.RET_OK:
        # Main loop to check the strategies
        get_market_data('127.0.0.1',
                        11111,
                        stock,
                        0.2, 0.8, ret_data)

    # Disconnect to futu api
