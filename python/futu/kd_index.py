#!/usr/bin/python
from utilities import Logger, get_line_number
import pandas as pd

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
            index = stocks_df.index[i]
            date = stocks_df.iloc[i]['time_key']
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

            log += "{9} - Date:{0} High:{1:0.2f} Low:{2:0.2f} Close:{3:0.2f} Highest(N):{4:0.2f} Lowest(N):{5:0.2f} " \
                   "RSV:{6:0.4f} K:{7:0.4f} D:{8:0.4f}\n".format(date,
                                                                 high_price,
                                                                 low_price,
                                                                 close_price,
                                                                 highest_price,
                                                                 lowest_price,
                                                                 today_rsv,
                                                                 today_k,
                                                                 today_d,
                                                                 index)

            # add to lists
            data['date'].append(date)
            data['high'].append(format(high_price, '.2f'))
            data['low'].append(format(low_price, '.2f'))
            data['close'].append(format(close_price, '.2f'))
            data['highest'].append(format(highest_price, '.2f'))
            data['lowest'].append(format(lowest_price, '.2f'))
            data['rsv'].append(format(today_rsv, '.4f'))
            data['k'].append(format(today_k, '.4f'))
            data['d'].append(format(today_d, '.4f'))

        Logger.log_trace('L1', 'calculate_kd_with_data', get_line_number(), log)
        return data

    def append_new_data_to_datafrme(self, kd_df, kline_data):

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

        log = ''

        for index, row in kline_data.iterrows():
            # KDJ requires 9 days (include current price) data to find out the RSV
            df_max = kd_df[-8:].max()
            df_min = kd_df[-8:].min()

            # calculate the RSV
            date = row['time_key']

            if date in kd_df['date']:
                continue

            high_price = float(row['high'])
            low_price = float(row['low'])
            close_price = row['close']
            previous_k = float(kd_df.iloc[-1]['k'])
            previous_d = float(kd_df.iloc[-1]['d'])
            highest_price = max(high_price, float(df_max['high']))
            lowest_price = min(low_price, float(df_min['low']))
            today_rsv = (close_price - lowest_price) / (highest_price - lowest_price)

            # calculate the KD value
            today_k = self.calculate_today_k(previous_k, today_rsv)
            today_d = self.calculate_today_d(previous_d, today_k)

            log += "Date:{0} High:{1:0.2f} Low:{2:0.2f} Close:{3:0.2f} Highest(N):{4:0.2f} Lowest(N):{5:0.2f} " \
                   "RSV:{6:0.4f} K:{7:0.4f} D:{8:0.4f}\n".format(date,
                                                                 high_price,
                                                                 low_price,
                                                                 close_price,
                                                                 highest_price,
                                                                 lowest_price,
                                                                 today_rsv,
                                                                 today_k,
                                                                 today_d)

            # add to lists
            reference_data['date'].append(date)
            reference_data['high'].append(format(high_price, '.2f'))
            reference_data['low'].append(format(low_price, '.2f'))
            reference_data['close'].append(format(close_price, '.2f'))
            reference_data['highest'].append(format(highest_price, '.2f'))
            reference_data['lowest'].append(format(lowest_price, '.2f'))
            reference_data['rsv'].append(format(today_rsv, '.4f'))
            reference_data['k'].append(format(today_k, '.4f'))
            reference_data['d'].append(format(today_d, '.4f'))

        Logger.log_trace('L1', 'calculate_kd_with_data', get_line_number(), log)

        new_kd_df = pd.DataFrame(data=reference_data, index=reference_data['date'])
        # Logger.log_trace('L1', 'trade_report', get_line_number(), new_kd_df)

        return kd_df.append(new_kd_df)

    def check_new_kd_with_price(self, kd_df, price):
        # KDJ requires 9 days (include current price) data to find out the RSV
        df_max = kd_df[-8:].max()
        df_min = kd_df[-8:].min()

        # calculate the RSV
        close_price = price
        previous_k = float(kd_df.iloc[-1]['k'])
        previous_d = float(kd_df.iloc[-1]['d'])
        highest_price = max(price, float(df_max['high']))
        lowest_price = min(price, float(df_min['low']))
        today_rsv = (close_price - lowest_price) / (highest_price - lowest_price)

        # calculate the KD value
        today_k = self.calculate_today_k(previous_k, today_rsv)
        today_d = self.calculate_today_d(previous_d, today_k)

        return today_k, today_d

