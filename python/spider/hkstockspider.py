import pandas_datareader as data
import pandas as pd
from datetime import datetime

# We would like all available data from 01/01/2000 until 12/31/2016.
start_date = '2018-08-01'
end_date = '2018-08-31'

stock_code = '2800.HK'
start = datetime(2018, 8, 22)
end = datetime(2018, 9, 22)

# User pandas_reader.data.DataReader to load the desired data. As simple as that.
# df = data.get_data_yahoo('2800.hk', start_date, end_date)
df = data.get_data_yahoo(stock_code, start=start, end=end)

print(len(df.columns))
print(df.columns)

print(len(df.index))
print(df.head())
# print("--------------------")
# print(df.iloc[0:15]) # from 0 to 2
# print("--------------------")


# begin = 0
# end = 9
#
# # df_min = df.iloc[:9].min()
# df_max = df.iloc[begin:end].max()
# df_min = df.iloc[begin:end].min()
# Hn = df_max['High']
# Ln = df_min['Low']
#
# print("Max Df - High :{0}".format(df_max['High']))
# print("Min Df - High :{0}".format(df_min['High']))

num_of_row = len(df.index)
previous_K = 0
previous_D = 0

date_list = []
RSV_list = []
K_list = []
D_list = []

for i in range(8, num_of_row):
    end = i + 1
    begin = end - 9
    df_max = df.iloc[begin:end].max()
    df_min = df.iloc[begin:end].min()

    date = df.index[i]
    Hn = df_max['High']
    Ln = df_min['Low']
    Cn = df.iloc[i]['Close']
    RSV = (Cn-Ln)/(Hn-Ln)

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

    print("Date:{0} RSV:{1:0.4f} K:{2:0.4f} D:{3:0.4f}".format(date, RSV, today_K, today_D))
    date_list.append(date)
    RSV_list.append(RSV)
    K_list.append(today_K)
    D_list.append(today_D)

# data = np.array([RSV_list, K_list, D_list])
# print(data.shape)

data = {
        'RSV': RSV_list,
        'K': K_list,
        'D': D_list
    }

KD_dataframe = pd.DataFrame(data=data, index=date_list)

print(KD_dataframe.head())

