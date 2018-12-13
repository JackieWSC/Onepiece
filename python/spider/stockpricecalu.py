import pandas_datareader as data
import pandas as pd
from datetime import datetime


pd.set_option('display.max_columns',None)

# We would like all available data from 01/01/2000 until 12/31/2016.
start_date = '2007-08-01'
end_date = '2018-08-31'

stock_code = '0700.HK'
stock_code = '^HSI'
start = datetime(2016, 1, 1)
end = datetime(2018, 9, 30)

# User pandas_reader.data.DataReader to load the desired data. As simple as that.
# df = data.get_data_yahoo('2800.hk', start_date, end_date)
# the early start day is 2007-12-31
df = data.get_data_yahoo(stock_code, start=start, end=end)

print(len(df.columns))
print(df.columns)

no_of_record = len(df.index)
print(len(df.index))

print(df.head(5))
print(df.tail(5))
# print("--------------------")
# print(df.iloc[0:15]) # from 0 to 2
# print("--------------------")

# close_price_df = df[['Close']].copy()
# print(close_price_df.head(10))

df['Close'] = round(df['Close'],-1)

new = df.groupby(['Close']) \
        .size() \
        .reset_index(name='Close count') \
        .sort_values(['Close'], ascending=True)
# print(new)
new["Percentage"] = round((new['Close count'] / no_of_record) * 100, 1)
new['Stock'] = '2800.HK'
new['Period'] = '10'
new['Remark'] = '{0} to {1}'.format(start.strftime("%Y-%m-%d"), end.strftime("%Y-%m-%d"))
print(new)


