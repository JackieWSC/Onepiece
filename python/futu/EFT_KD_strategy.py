#!/usr/bin/python
import futu as ft
import pandas as pd
from kd_index import KDIndex
from utilities import Logger, get_line_number


def get_stock_data(host, port, stock, start_date, end_date):
    quote_ctx = ft.OpenQuoteContext(host, port)

    # 2800ETF
    # start_date = '2018-01-02'
    # end_date = '2018-12-31'
    ret, data_frame, page_req_key = quote_ctx.request_history_kline(stock,
                                                                    start_date,
                                                                    end_date,
                                                                    ktype=ft.KLType.K_30M,
                                                                    autype=ft.AuType.NONE,
                                                                    fields=[ft.KL_FIELD.DATE_TIME,
                                                                            ft.KL_FIELD.OPEN,
                                                                            ft.KL_FIELD.CLOSE,
                                                                            ft.KL_FIELD.HIGH,
                                                                            ft.KL_FIELD.LOW],
                                                                    max_count=3000)
    print('Result:{}'.format(ret))
    print('Key:{}'.format(page_req_key))
    print('Data:\n{}', data_frame)

    quote_ctx.close()
    return data_frame


def dump_data_to_json(data_frame, filename):
    file = open(filename, 'w')
    file.write(str(data_frame.to_json(orient='records')))
    file.close()


def get_data_from_json(filename):
    data_frame = pd.read_json(filename, orient='columns')

    return data_frame


def regular_strategy_simulator(k_value, d_value, data_frame):
    print('K:{}, D:{}'.format(k_value, d_value))
    print(data_frame)

    base_account = 1000000  # init value in acc
    base_shou = 10  # buy 10 lots

    sum_account = 1000000  # money in acc
    sum_stoke = 0  # total lots
    sum_value = 0  # total value
    sum_gain_loss_rate = 0  # net profile
    sum_fee = 0  # total fee
    trade_type = 0  # type of type

    chicang_rate = 0  # position net profile
    chicang_stoke_avg_cost = 0  # stock cost

    last_price = 0  # stock price at the end date

    dingtou_base = 100000  # money used for each time
    dingtou_cycle = 20  # trading cycle
    clear_count = 0  # time of clear the book

    start_time = '2019-01-02'
    end_time = '2019-12-31'

    for index, row in data_frame.iterrows():
        # print('Index:{}'.format(index))
        # print('open:{}'.format(row['open']))

        last_price = row['close']
        time_key = row['time_key']

        stoke = 0
        one_stoke_price = last_price * 1000
        one_unit_stoke = int(dingtou_base/one_stoke_price)

        start_chicang_stoke_avg_cost = chicang_stoke_avg_cost
        start_chicang_rate = 0
        if (chicang_stoke_avg_cost == 0):
            start_chicang_rate = 0
        else:
            start_chicang_rate = ((last_price - chicang_stoke_avg_cost) / chicang_stoke_avg_cost)

        if row['time_key'] < start_time:
            continue

        if row['time_key'] > end_time:
            break

        if sum_stoke == 0:
            trade_type = "Empty Position, Buy One Unit"
            stoke = one_unit_stoke

            chicang_rate = 0
            chicang_stoke_avg_cost = last_price
        else:
            if index % dingtou_cycle == 0 and sum_account > 0:
                stoke = one_unit_stoke
                trade_type = "Cycle reach, But One Unit"

                chicang_stoke_avg_cost = ((sum_stoke * chicang_stoke_avg_cost) + (stoke * last_price)) / (sum_stoke + stoke)

                chicang_rate = (last_price - chicang_stoke_avg_cost) / chicang_stoke_avg_cost

        if stoke == 0 or sum_account < (dingtou_base * 1.2):
            continue

        sum_stoke += stoke
        sum_fee += 15
        sum_account -= ((stoke * one_stoke_price) + 15)
        sum_value = sum_account + (sum_stoke * one_stoke_price)
        sum_gain_loss_rate = ((sum_value - base_account) / base_account) * 100

        trade_report = '''
---- {timeKey} ({index})--{tradeType}--{oneUnitStoke} (Stoke) ----
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
      Transaction Fee: ${sumFee}
'''.format(timeKey=time_key,
           index=index,
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

        print(trade_report)

    summary_report = ''
    print(summary_report)


def kd_strategy_simulator(buy_in_k_value, sell_out_k_value, data_frame):
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

    for index, row in kd_df.iterrows():

        k = float(row['k'])
        d = float(row['d'])
        last_price = float(row['close'])

        # when buy
        sell_signal = k > sell_out_k_value

        # when sell
        buy_signal = k < buy_in_k_value

        time_key = row['date']

        text = ""

        if buy_signal is True:
            text = "BUY"

        if sell_signal is True:
            text = "SELL"

        log = '{} ${} ({},{}) {} {} {}'.format(index, last_price, k, d, buy_signal, sell_signal, text)
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
            continue

        sum_stoke += stoke
        sum_fee += 15
        sum_account -= ((stoke * one_stoke_price) + 15)
        sum_value = sum_account + (sum_stoke * one_stoke_price)
        sum_gain_loss_rate = ((sum_value - base_account) / base_account) * 100

        trade_report = '''
---- {timeKey} ({index})--{tradeType}--{oneUnitStoke} (Stoke) ----
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
'''.format(timeKey=time_key,
           index=index,
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


def append_kd_testing(testing, buy_in, sell_out):
    testing['buy_in'].append(buy_in)
    testing['sell_out'].append(sell_out)


# base on the start, end and step to generate the different KD Buy/Sell indicator
#   e.g. Start = 20
#       End = 90
#       Step = 10
#   it will create follow Buy Sell Indicator
#     (20,55) (20,65) (20,75) (20,85)
#     (30,55) (30,65) (30,75) (30,85)
#     (40,55) (40,65) (40,75) (40,85)
def append_kd_testing_adv(testing, start, end, step):
    for i in range(start, 50, step):
        for j in range(60, end, step):
            testing['buy_in'].append(i/100)
            testing['sell_out'].append(j/100)


if __name__ == "__main__":

    fetch_data = False
    simulator = True
    file_name = '2800_2019_30M_data.json'

    # fetch the data from futu api to json file
    if fetch_data is True:
        data_frame = get_stock_data(host='127.0.0.1',
                                    port=11111,
                                    stock='HK.02800',
                                    start_date='2019-01-02',
                                    end_date='2019-12-31')
        dump_data_to_json(data_frame, file_name)

    # read the data from json file
    data_frame = get_data_from_json(file_name)

    # run the simulator to back test the data
    if len(data_frame.index) > 0 and simulator is True:

        kd_result = {
            'buy_in': [],
            'sell_out': []
        }

        # append_kd_testing(kd_result, 0.15, 0.85)
        # append_kd_testing(kd_result, 0.15, 0.80)
        # append_kd_testing(kd_result, 0.15, 0.75)
        # append_kd_testing(kd_result, 0.15, 0.70)
        # append_kd_testing(kd_result, 0.15, 0.65)
        #
        # append_kd_testing(kd_result, 0.20, 0.85)
        # append_kd_testing(kd_result, 0.20, 0.80)
        # append_kd_testing(kd_result, 0.20, 0.75)
        # append_kd_testing(kd_result, 0.20, 0.70)
        # append_kd_testing(kd_result, 0.20, 0.65)
        #
        append_kd_testing_adv(kd_result, 10, 95, 10)

        # go to test different KD combination
        kd_dataframe = pd.DataFrame(kd_result, columns=['buy_in', 'sell_out'])
        # print(kd_dataframe)

        # run the back test with different KD combination
        gain_loss = []
        for index, row in kd_dataframe.iterrows():
            buy_in = row['buy_in']
            sell_out = row['sell_out']
            gain_loss.append(kd_strategy_simulator(buy_in,
                                                   sell_out,
                                                   data_frame))

        # dump the summary report
        kd_dataframe['gain_loss'] = gain_loss
        kd_dataframe.sort_values(by=['gain_loss'], ascending=False, inplace=True)
        pd.set_option('display.max_rows', kd_dataframe.shape[0]+1)
        print(kd_dataframe)


