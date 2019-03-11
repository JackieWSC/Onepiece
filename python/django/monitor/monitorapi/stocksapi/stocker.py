import datetime
import pandas
import pandas_datareader as datareader
import requests
from stocksapi.models import StockPriceStatistics, StockDailyInfo, StockKDInfo
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

    @staticmethod
    def get_close_price(stock_code):
        end_date = datetime.date.today()
        start_date = datetime.date.today()
        stocks_df = datareader.get_data_yahoo(stock_code, start=start_date, end=end_date)
        stocks_df.rename(str.lower, axis='columns', inplace=True)
        close_price = stocks_df['close']
        return close_price

    @staticmethod
    def calculate_price_tick(close_price):
        if close_price > 1000:
            price_tick = 100
        elif close_price > 100:
            price_tick = 1
        elif close_price > 10:
            price_tick = 0.1
        elif close_price > 5:
            price_tick = 0.05
        elif close_price > 1:
            price_tick = 0.01
        else:
            price_tick = 0.005

        return price_tick

    def check_price_tick(self, stock_code):
        if stock_code in self.stock_price_tick:
            price_tick = self.stock_price_tick[stock_code]
        else:
            # use the today close price to calculate the price tick
            close_price_str = self.get_close_price(stock_code)
            close_price = float(close_price_str)
            price_tick = self.calculate_price_tick(close_price)

        log = 'Price Tick for {0} is {1}'.format(stock_code, price_tick)
        Logger.log_trace('L2', 'check_price_tick', get_line_number(), log)
        return price_tick

    def get_stock_name(self, stock_code):
        stock_code = self.check_stock_code(stock_code)

        link = "http://d.yimg.com/autoc.finance.yahoo.com/autoc?query={}&region=1&lang=en".format(stock_code)
        result = requests.get(link).json()
        stock_name = ""

        for data in result['ResultSet']['Result']:
            if data['symbol'] == stock_code:
                stock_name = data['name']

        return stock_name

    def get_stock_dataframe(self, stock_code, start_date=None, end_date=None):
        stock_code = self.check_stock_code(stock_code)

        if end_date is None:
            end_date = datetime.date.today()

        if start_date is None:
            start_date = end_date - datetime.timedelta(days=50)

        stocks_df = datareader.get_data_yahoo(stock_code, start=start_date, end=end_date)
        stocks_df.rename(str.lower, axis='columns', inplace=True)
        print(stocks_df.columns)
        num_of_row = len(stocks_df.index)

        log = "Yahoo API Start Date:{0} Stock:{1} Dataframe Size:{2} ".format(
            start_date.strftime('%Y-%m-%d'),
            stock_code,
            num_of_row)
        Logger.log_trace('L2', 'get_stock_dataframe', get_line_number(), log)

        return stock_code, stocks_df

    def get_stock_dataframe_from_db(self, stock_code, year, all_data=False):
        stock_code = self.check_stock_code(stock_code)
        # all_entries = StockDailyInfo.objects.all()
        # for entry in all_entries:
        #     log = "{0} {1} {2} {3}".format(entry.date, entry.high, entry.low, entry.close)
        #     Logger.log_trace('L2', 'get_stock_dataframe_from_db', get_line_number(), log)

        if all_data:
            db_data = StockDailyInfo.objects.filter(
                stock=stock_code
            ).order_by('date')

        else:
            db_data = StockDailyInfo.objects.filter(
                stock=stock_code,
                date__year=year,
            ).order_by('date')

        temp_df = pandas.DataFrame.from_records(db_data.values())

        # print(temp_df.columns)
        # Rename the column to Date, High, Low, Close which match yahoo api
        # temp_df.rename(inplace=True, columns={
        #     'date': 'Date',
        #     'stock': 'Stock',
        #     'high': 'High',
        #     'low': 'Low',
        #     'close': 'Close'
        # })
        # print(temp_df.columns)

        return stock_code, temp_df

    def get_kd_dataframe_from_db(self, stock_code, year):
        stock_code = self.check_stock_code(stock_code)
        # all_entries = StockDailyInfo.objects.all()
        # for entry in all_entries:
        #     log = "{0} {1} {2} {3}".format(entry.date, entry.high, entry.low, entry.close)
        #     Logger.log_trace('L2', 'get_stock_dataframe_from_db', get_line_number(), log)

        db_data = StockKDInfo.objects.filter(
            stock=stock_code,
            date__year=year,
        ).order_by('date')

        temp_df = pandas.DataFrame.from_records(db_data.values())

        # print(temp_df.columns)
        # Rename the column to Date, High, Low, Close which match yahoo api
        # temp_df.rename(inplace=True, columns={
        #     'date': 'Date',
        #     'stock': 'Stock',
        #     'high': 'High',
        #     'low': 'Low',
        #     'close': 'Close'
        # })
        # print(temp_df.columns)

        return stock_code, temp_df

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

    def create_kd_index(self, stock_code):
        # get the stock data from pandas_datareader
        #   e.g. stock_code = '2800.HK'
        #   e.g. start = datetime.datetime(2018, 8, 22)get_stock_dataframe
        stock_code, stocks_df = self.get_stock_dataframe(stock_code)

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

        reference_data = self.calculate_kd_with_data(stocks_df, reference_data)

        # not show all records in json only create last 20 trading day (display_trading_day)
        kd_df = pandas.DataFrame(data=reference_data, index=reference_data['date'])

        display_trading_day = 20
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
        close_price = float(reference_data['close'][-1])
        highest_price = float(reference_data['highest'][-1])
        lowest_price = float(reference_data['lowest'][-1])
        previous_k = float(reference_data['k'][-1])
        log = ''
        if direction in 'UP':
            price_direction = 1
        elif direction in 'DOWN':
            price_direction = -1

        for i in range(1, num_of_date):
            next_close = close_price + ((i * stock_price_tick) * price_direction)
            k = self.predict_k(next_close, highest_price, lowest_price, previous_k)

            k_str = format(k, '.4f')
            if data['k'][-1] == k_str:
                break

            data['close'].append(format(close_price, '.2f'))
            data['price'].append(format(next_close, '.2f'))
            data['k'].append(k_str)
            data['type'].append(direction)

            log += "Type:{0} Next Close:{1} K:{2}\n".format(direction,
                                                            format(next_close, '.2f'),
                                                            k_str)

        Logger.log_trace('L2', 'predict_next_k', get_line_number(), log)

    @staticmethod
    def notify_line(send, date, close_price, k_value):
        if send:
            is_weekday = datetime.datetime.today().weekday() < 5
            if is_weekday:
                if k_value < 0.25 or k_value > 0.65:
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

    @staticmethod
    def stock_list_notify_line(send, date, data):

        text = "{}\n".format(date)

        for i in range(0, len(data['Price'])):
            k_value = format(data['K'][i] * 100, '.0f')
            d_value = format(data['D'][i] * 100, '.0f')

            text += '{} ${:>5} KD({}% {}%)\n'.format(
                data['Stock'][i],
                data['Price'][i],
                k_value,
                d_value)

        log = text
        Logger.log_trace('L2', 'stock_list_notify_line', get_line_number(), log)

        if send:
            is_weekday = datetime.datetime.today().weekday() < 5
            if is_weekday:

                IFTTT_WEBHOOKS_URL = 'https://maker.ifttt.com/trigger/{}/with/key/{}'
                event = 'stocklistLine'
                token = 'jSfmLiQN7-TxzISuY3kE6p-gusxDr3CTivpaHqNWFCG'

                url_ifttt = IFTTT_WEBHOOKS_URL.format(event, token)
                log = "IFTTT URL:{0}".format(url_ifttt)
                Logger.log_trace('L2', 'stock_list_notify_line', get_line_number(), log)

                # payload
                data = {
                    'value1': text
                }

                # send the request
                req = requests.post(url_ifttt, data)
                log = 'Request Text:{0}'.format(req.text)
                Logger.log_trace('L2', 'stock_list_notify_line', get_line_number(), log)

    def create_next_kd_index(self, stock_code, send_to_line=False):
        # get the stock data from pandas_datareader
        #   e.g. stock_code = '2800.HK'
        #   e.g. start = datetime.datetime(2018, 8, 22)
        stock_code, stocks_df = self.get_stock_dataframe(stock_code)

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

        reference_data = self.calculate_kd_with_data(stocks_df, reference_data)
        date = reference_data['date'][-1]
        close_price = float(reference_data['close'][-1])
        previous_k = float(reference_data['k'][-1])
        highest_price = float(max(reference_data['high'][-9:]))
        lowest_price = float(min(reference_data['low'][-9:]))

        data = {
            'close': [],
            'price': [],
            'k': [],
            'type': []
        }

        highest_price_list = reference_data['high'][-9:]
        lowest_price_list = reference_data['low'][-9:]

        log = 'highest_price_list: {}, lowest_price_list:{}'.format(
            highest_price_list,
            lowest_price_list)
        Logger.log_trace('L2', 'create_next_kd_index', get_line_number(), log)

        log = 'highest_price: {}, lowest_price:{}'.format(
            highest_price,
            lowest_price)
        Logger.log_trace('L2', 'create_next_kd_index', get_line_number(), log)

        # first 1
        k = self.predict_k(close_price, highest_price, lowest_price, previous_k)
        data['close'].append(format(close_price, '.2f'))
        data['price'].append(format(close_price, '.2f'))
        data['k'].append(format(k, '.4f'))
        data['type'].append("START")

        # send the notification to line
        self.notify_line(send_to_line, date, close_price, previous_k)

        # calculate next +/- price and related KD value
        self.predict_next_k(reference_data, stock_code, "UP", 10, data)
        self.predict_next_k(reference_data, stock_code, "DOWN", 10, data)

        kd_df = pandas.DataFrame(data=data)
        kd_df.sort_values('price', inplace=True)

        return kd_df.to_json(orient='records')

    @staticmethod
    def get_monitor_stock_list():
        # read the list from database
        stock_list = [
            "2800.HK",
            "2833.HK",
            "3115.HK",
            "3140.HK",
            "3019.HK"
        ]

        return stock_list

    def calculate_stock_list_kd(self, send_to_line):
        # get the stock_list from database
        stock_list = self.get_monitor_stock_list()

        result = {
            'Stock': [],
            'Price': [],
            'K': [],
            'D': []
        }

        # get the latest record
        for stock in stock_list:
            stock_code, stocks_df = self.get_stock_dataframe(stock)

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

            reference_data = self.calculate_kd_with_data(stocks_df, reference_data)
            close_price = float(reference_data['close'][-1])
            k_value = float(reference_data['k'][-1])
            d_value = float(reference_data['d'][-1])

            result['Stock'].append(stock_code)
            result['Price'].append(close_price)
            result['K'].append(k_value)
            result['D'].append(d_value)

            log = 'Check KD of stock: {}\n' \
                  '  Price:{}, K:{}, D:{}'.format(stock, close_price, k_value, d_value)
            Logger.log_trace('L2', 'calculate_stock_list_kd', get_line_number(), log)

        # save the kd of each stock to database
        date = reference_data['date'][-1]
        self.stock_list_notify_line(send_to_line, date, result)

    def create_stock_price_history(self, stock_code, year):
        start, year = self.check_start_date(year)
        end = datetime.date.today()
        stock_code = self.check_stock_code(stock_code)

        # User pandas_reader.data.DataReader to load the desired data. As simple as that.
        # df = data.get_data_yahoo('2800.hk', start_date, end_date)
        # the early start day is 2007-12-31
        stock_df = datareader.get_data_yahoo(stock_code, start=start, end=end)
        stock_df.rename(str.lower, axis='columns', inplace=True)
        no_of_record = len(stock_df.index)

        print('create_stock_price_history - no_of_record', no_of_record)

        # round the price to 1 decimal
        decimal = self.get_decimal(stock_code)
        stock_df['price'] = round(stock_df['close'], decimal)

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

    def get_db_data(self, stock_code, year):
        # get the stock data from pandas_datareader
        #   e.g. stock_code = '2800.HK'
        #   e.g. start = datetime.datetime(2018, 8, 22)
        stock_code, stocks_df = self.get_stock_dataframe_from_db(stock_code, year)

        log = "year:{0} \n  stocks_df size:{1}".format(year, stocks_df.size)
        Logger.log_trace('L2', 'get_db_data', get_line_number(), log)

        if not stocks_df.empty:
            stocks_df['date'] = stocks_df['date'].map('{:%Y-%m-%d}'.format)

            # remove useless column
            stocks_df.drop(['id'], axis=1, inplace=True)

        return stocks_df.to_json(orient='records')

    def get_db_kd_data(self, stock_code, year):
        # get the stock data from pandas_datareader
        #   e.g. stock_code = '2800.HK'
        #   e.g. start = datetime.datetime(2018, 8, 22)
        stock_code, stocks_df = self.get_kd_dataframe_from_db(stock_code, year)

        if not stocks_df.empty:
            # stocks_df.reset_index(inplace=True)
            stocks_df['date'] = stocks_df['date'].map('{:%Y-%m-%d}'.format)

            # remove useless column
            stocks_df.drop(['id'], axis=1, inplace=True)

        return stocks_df.to_json(orient='records')

    # use the yahoo api data to create the raw data to database for subsequence calculation
    # key: date + stock
    # fields:
    # - date
    # - stock
    # - high
    # - low
    # - close
    def create_api_data_to_db(self, stock_code, year, input_type):
        # get the stock data from pandas_datareader
        #   e.g. stock_code = '2800.HK'
        #   e.g. start = datetime.datetime(2018, 8, 22)
        stock_code, stocks_df = self.get_stock_dataframe(stock_code,
                                                         datetime.datetime(year, 1, 2),
                                                         datetime.datetime(year, 12, 31))

        stocks_df.reset_index(inplace=True)

        log = "Columns:{0} ".format(stocks_df.columns)
        Logger.log_trace('L2', 'create_api_data_to_db', get_line_number(), log)

        stocks_df['date'] = stocks_df['Date'].dt.strftime('%Y-%m-%d')
        stocks_df['high'] = stocks_df['high'].map('{:.2f}'.format)
        stocks_df['low'] = stocks_df['low'].map('{:.2f}'.format)
        stocks_df['open'] = stocks_df['open'].map('{:.2f}'.format)
        stocks_df['close'] = stocks_df['close'].map('{:.2f}'.format)
        stocks_df['volume'] = stocks_df['volume'].map('{:.2f}'.format)
        stocks_df['adj close'] = stocks_df['adj close'].map('{:.2}'.format)
        stocks_df['stock'] = stock_code
        # remove useless column
        stocks_df.drop(['Date'], axis=1, inplace=True)

        write_to_db = (input_type == "jackie")

        log = "write_to_db:{0} \n  input_type:{1}".format(write_to_db, input_type)
        Logger.log_trace('L2', 'create_api_data_to_db', get_line_number(), log)

        # write the data to database
        if write_to_db:
            # create the another dataframe from stocks dataframe and save to database
            temp_df = pandas.DataFrame({
                "date": stocks_df['date'],
                "high": stocks_df['high'],
                "low": stocks_df['low'],
                "close": stocks_df['close'],
                "stock": stock_code
            })

            entries = []
            # for entry in stocks_df.T.to_dict().values():
            for entry in temp_df.to_dict('records'):
                # print(entry)
                entries.append(StockDailyInfo(**entry))

            StockDailyInfo.objects.bulk_create(entries)

        return stocks_df.to_json(orient='records')

    def create_kd_data_to_db(self, stock_code, input_type):
        # get the data from db
        # calculate the KD
        # save to db
        # get the stock data from pandas_datareader
        #   e.g. stock_code = '2800.HK'
        #   e.g. start = datetime.datetime(2018, 8, 22)get_stock_dataframe
        stock_code, stocks_df = self.get_stock_dataframe_from_db(stock_code, "", True)

        # stocks_df['Date'] = stocks_df['Date'].map('{:%Y-%m-%d}'.format)
        stocks_df.set_index('date', inplace=True)

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

        reference_data = self.calculate_kd_with_data(stocks_df, reference_data)

        kd_df = pandas.DataFrame(data=reference_data, index=reference_data['date'])
        kd_df.reset_index(inplace=True)
        kd_df["stock"] = stock_code

        # remove useless column
        kd_df.drop(['index'], axis=1, inplace=True)

        write_to_db = (input_type == "jackie")

        log = "write_to_db:{0} \n  input_type:{1}".format(write_to_db, input_type)
        Logger.log_trace('L2', 'create_kd_data_to_db', get_line_number(), log)

        # write the data to database
        if write_to_db:
            # create the another dataframe from stocks dataframe and save to database
            # temp_df = pandas.DataFrame({
            #     "date": kd_df['Date'],
            #     "stock": stock_code,
            #     "high": kd_df['High'],
            #     "low": kd_df['Low'],
            #     "close": kd_df['Close'],
            #     "highest": kd_df['Highest'],
            #     "lowest": kd_df['Lowest'],
            #     "rsv": kd_df['RSV'],
            #     "k": kd_df['K'],
            #     "d": kd_df['D'],
            # })

            entries = []
            for entry in kd_df.to_dict('records'):
                # print(entry)
                entries.append(StockKDInfo(**entry))

            StockKDInfo.objects.bulk_create(entries)

        return kd_df.to_json(orient='records')
