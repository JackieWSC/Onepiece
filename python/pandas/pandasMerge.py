import pandas as pd

# reference
# https://github.com/shanealynn/Pandas-Merge-Tutorial/blob/master/Pandas%20Merge%20Tutorial.ipynb
# https://www.shanelynn.ie/merge-join-dataframes-python-pandas-index-1/
# extract method: https://stackoverflow.com/questions/49382937/python-pandas-dataframe-str-contains-merge-if
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

user_usage = pd.read_csv("user_usage.csv")
user_device = pd.read_csv("user_device.csv")
devices = pd.read_csv("android_devices.csv")

print(user_usage.head())
print(user_device.head())
print(devices.head())

# panda merge is default inner join
print("\nPanda merge is default inner join:")
result = pd.merge(user_usage,
                 user_device[['use_id', 'platform', 'device']],
                 on='use_id')
print(result.head(50))

print("user_usage dimensions: {}".format(user_usage.shape))
print("user_device dimensions: {}".format(user_device[['use_id', 'platform', 'device']].shape))
print("result dimensions: {}".format(result.shape))

# left merge example
print("\nLeft merge example:")
result = pd.merge(user_usage,
                 user_device[['use_id', 'platform', 'device']],
                 on='use_id',
                 how='left')
print(result.head(50))

print("user_usage dimensions: {}".format(user_usage.shape))
print("user_device dimensions: {}".format(user_device[['use_id', 'platform', 'device']].shape))
print("result dimensions: {}".format(result.shape))
print("There are {} missing values in the result.".format(result["device"].isnull().sum()))


# Now, based on the "device" column in result, match the "Model" column in devices.
devices.rename(columns={"Retail Branding": "manufacturer"}, inplace=True)
result = pd.merge(result,
                  devices[['manufacturer', 'Model']],
                  left_on='device',
                  right_on='Model',
                  how='left')
print(result.head(50))
