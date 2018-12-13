import datetime
import pandas
import pandas_datareader as datareader
import requests
from stocksapi.models import StockPriceStatistics
from stocksapi.utilities import Logger, get_line_number


class Stocker:
    stock_decimal = {
        "2800.HK": 1,
        "^HSI": -2,
    }

    stock_price_tick = {
        "2800.HK": 0.1,
        "^HSI": 100,
    }

    @classmethod
    def get_decimal(cls, stock_code):
        return cls.stock_decimal[stock_code]

    @staticmethod
    def check_stock_code(stock_code):
        if stock_code == "HSI":
            stock_code = "^HSI"
        return stock_code

    @classmethod
    def check_price_tick(cls, stock_code):
        return cls.stock_price_tick[stock_code]

    @staticmethod
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

    def get_stock_name(self, stock_code):
        stock_code = self.check_stock_code(stock_code)

        link = "http://d.yimg.com/autoc.finance.yahoo.com/autoc?query={}&region=1&lang=en".format(stock_code)
        result = requests.get(link).json()
        stock_name = ""

        for data in result['ResultSet']['Result']:
            if data['symbol'] == stock_code:
                stock_name = data['name']

        return stock_name

    def get_stock_dataframe(self, stock_code):
        stock_code = self.check_stock_code(stock_code)
        end_date = datetime.date.today()
        start_date = end_date - datetime.timedelta(days=50)
        stocks_df = datareader.get_data_yahoo(stock_code, start=start_date, end=end_date)
        return stock_code, stocks_df

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
            highest_price = df_max['High']
            lowest_price = df_min['Low']
            high_price = stocks_df.iloc[i]['High']
            low_price = stocks_df.iloc[i]['Low']
            close_price = stocks_df.iloc[i]['Close']
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

            data['Date'].append(date.strftime('%Y-%m-%d'))
            data['HighN'].append(format(highest_price, '.2f'))
            data['LowN'].append(format(lowest_price, '.2f'))
            data['Close'].append(format(close_price, '.2f'))
            data['RSV'].append(format(today_rsv, '.4f'))
            data['K'].append(format(today_k, '.4f'))
            data['D'].append(format(today_d, '.4f'))

        Logger.log_trace('L2', 'calculate_kd_with_data', get_line_number(), log)
        return data

    def create_kd_index(self, stock_code):
        # get the stock data from pandas_datareader
        #   e.g. stock_code = '2800.HK'
        #   e.g. start = datetime.datetime(2018, 8, 22)get_stock_dataframe
        stock_code, stocks_df = self.get_stock_dataframe(stock_code)
        display_trading_day = 20

        reference_data = {
            'Date': [],
            'HighN': [],
            'LowN': [],
            'Close': [],
            'RSV': [],
            'K': [],
            'D': []
        }

        reference_data = self.calculate_kd_with_data(stocks_df, reference_data)

        # not show all records in json only create last 20 trading day (display_trading_day)
        kd_df = pandas.DataFrame(data=reference_data, index=reference_data['Date'])
        kd_df = kd_df.iloc[-display_trading_day:]

        return kd_df.to_json(orient='records')

    def predict_k(self, close_price, highest_price, lowest_price, previous_k):
        if close_price < lowest_price:
            lowest_price = close_price

        if close_price > highest_price:
            highest_price = close_price

        rsv = (close_price - lowest_price) / (highest_price - lowest_price)
        k_value = self.calculate_today_k(previous_k, rsv)

        log = "Close:{0} K:{1} RSV:{2}".format(close_price, k_value, rsv)
        Logger.log_trace('L3', 'predict_k', get_line_number(), log)

        return k_value

    def predict_next_k(self, reference_data, stock_code, direction, num_of_date, data):
        # get the price tick with stock code
        stock_price_tick = self.check_price_tick(stock_code)
        close_price = float(reference_data['Close'][-1])
        highest_price = float(reference_data['HighN'][-1])
        lowest_price = float(reference_data['LowN'][-1])
        previous_k = float(reference_data['K'][-1])
        log = ''
        if direction in 'UP':
            price_direction = 1
        elif direction in 'DOWN':
            price_direction = -1

        for i in range(1, num_of_date):
            next_close = close_price + ((i * stock_price_tick) * price_direction)
            k = self.predict_k(next_close, highest_price, lowest_price, previous_k)

            k_str = format(k, '.4f')
            if data['K'][-1] == k_str:
                break

            data['Close'].append(format(close_price, '.2f'))
            data['Price'].append(format(next_close, '.2f'))
            data['K'].append(k_str)
            data['Type'].append(direction)

            log += "Type:{0} Next Close:{1} K:{2}\n".format(direction,
                                                            format(next_close, '.2f'),
                                                            k_str)

        Logger.log_trace('L2', 'predict_next_k', get_line_number(), log)

    @staticmethod
    def notify_line(send, date, close_price, k_value):
        if send:
            k_value = format(k_value * 100, '.0f')

            log = "notify line - date:{0}, close_price:{1}, k_value:{2}".format(
                    date,
                    close_price,
                    k_value)
            Logger.log_trace('L2', 'notify_line', get_line_number(), log)

            IFTTT_WEBHOOKS_URL = 'https://maker.ifttt.com/trigger/{}/with/key/{}'
            event = 'stockLine'
            token = 'jSfmLiQN7-TxzISuY3kE6p-gusxDr3CTivpaHqNWFCG'

            url_ifttt = IFTTT_WEBHOOKS_URL.format(event, token)
            log = "IFTTT URL:{0}".format(url_ifttt);
            Logger.log_trace('L2', 'notify_line', get_line_number(), log)

            # payload
            data = {
                'value1': date,
                'value2': close_price,
                'value3': k_value
            }

            # send the request
            req = requests.post(url_ifttt, data)
            log = 'Request Text:{0}'.format(req.text)
            Logger.log_trace('L2', 'notify_line', get_line_number(), log)

    def create_next_kd_index(self, stock_code, send_to_line=False):
        # get the stock data from pandas_datareader
        #   e.g. stock_code = '2800.HK'
        #   e.g. start = datetime.datetime(2018, 8, 22)
        stock_code, stocks_df = self.get_stock_dataframe(stock_code)

        reference_data = {
            'Date': [],
            'HighN': [],
            'LowN': [],
            'Close': [],
            'RSV': [],
            'K': [],
            'D': []
        }

        reference_data = self.calculate_kd_with_data(stocks_df, reference_data)
        date = reference_data['Date'][-1]
        close_price = float(reference_data['Close'][-1])
        highest_price = float(reference_data['HighN'][-1])
        lowest_price = float(reference_data['LowN'][-1])
        previous_k = float(reference_data['K'][-1])

        data = {
            'Close': [],
            'Price': [],
            'K': [],
            'Type': []
        }

        # first 1
        k = self.predict_k(close_price, highest_price, lowest_price, previous_k)
        data['Close'].append(format(close_price, '.2f'))
        data['Price'].append(format(close_price, '.2f'))
        data['K'].append(format(k, '.4f'))
        data['Type'].append("START")

        # send the notification to line
        self.notify_line(send_to_line, date, close_price, previous_k)

        # calculate next +/- price and related KD value
        self.predict_next_k(reference_data, stock_code, "UP", 10, data)
        self.predict_next_k(reference_data, stock_code, "DOWN", 10, data)

        kd_df = pandas.DataFrame(data=data)
        kd_df.sort_values('Price', inplace=True)

        return kd_df.to_json(orient='records')

    def create_stock_price_history(self, stock_code, year):
        start, year = self.check_start_date(year)
        end = datetime.date.today()
        stock_code = self.check_stock_code(stock_code)

        # User pandas_reader.data.DataReader to load the desired data. As simple as that.
        # df = data.get_data_yahoo('2800.hk', start_date, end_date)
        # the early start day is 2007-12-31
        stock_df = datareader.get_data_yahoo(stock_code, start=start, end=end)
        no_of_record = len(stock_df.index)

        print('create_stock_price_history - no_of_record', no_of_record)

        # round the price to 1 decimal
        decimal = self.get_decimal(stock_code)
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
