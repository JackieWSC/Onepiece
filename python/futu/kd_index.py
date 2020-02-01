#!/usr/bin/python
import pandas as pd
import pandas_datareader as datareader
from utilities import Logger, get_line_number


class KDIndex:
    @staticmethod
    def calculate_today_k(previous_k, today_rsv):
        if previous_k != 0:
            today_k = ((1 / 3) * today_rsv) + ((2 / 3) * previous_k)
        else:
            today_k = (1 / 2) * today_rsv
        return today_k

    @staticmethod
    def calculate_today_d(previous_d, today_k):
        if previous_d != 0:
            today_d = ((1 / 3) * today_k) + ((2 / 3) * previous_d)
        else:
            today_d = (1 / 2) * today_k
        return today_d

    def calculate_kd_with_data(self, stocks_df, data):
        # temp variable
        num_of_row = len(stocks_df.index)
        previous_k = 0
        previous_d = 0
        log = ''

        # KDJ requires 9 days data to find out the RSV value first
        for i in range(8, num_of_row):
            end_date = i + 1
            begin = end_date - 9
            df_max = stocks_df.iloc[begin:end_date].max()
            df_min = stocks_df.iloc[begin:end_date].min()

            # calculate the RSV
            date = stocks_df.index[i]
            high_price = float(stocks_df.iloc[i]['high'])
            low_price = float(stocks_df.iloc[i]['low'])
            close_price = float(stocks_df.iloc[i]['close'])
            highest_price = float(df_max['high'])
            lowest_price = float(df_min['low'])
            today_rsv = (close_price - lowest_price) / (highest_price - lowest_price)

            # calculate the KD value
            today_k = self.calculate_today_k(previous_k, today_rsv)
            today_d = self.calculate_today_d(previous_d, today_k)

            previous_k = today_k
            previous_d = today_d

            # add to lists
            log += "Date:{0} High:{1:0.2f} Low:{2:0.2f} Close:{3:0.2f} Highest(N):{4:0.2f} Lowest(N):{5:0.2f} " \
                   "RSV:{6:0.4f} K:{7:0.4f} D:{8:0.4f}\n".format(date.strftime('%Y-%m-%d'),
                                                                 high_price,
                                                                 low_price,
                                                                 close_price,
                                                                 highest_price,
                                                                 lowest_price,
                                                                 today_rsv,
                                                                 today_k,
                                                                 today_d)

            data['date'].append(date.strftime('%Y-%m-%d'))
            data['high'].append(format(high_price, '.2f'))
            data['low'].append(format(low_price, '.2f'))
            data['close'].append(format(close_price, '.2f'))
            data['highest'].append(format(highest_price, '.2f'))
            data['lowest'].append(format(lowest_price, '.2f'))
            data['rsv'].append(format(today_rsv, '.4f'))
            data['k'].append(format(today_k, '.4f'))
            data['d'].append(format(today_d, '.4f'))

        Logger.log_trace('L2', 'calculate_kd_with_data', get_line_number(), log)
        return data
