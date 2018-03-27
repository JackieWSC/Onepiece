# Lesson 3 - Basio IO
# - read csv file
# - write csv file

import pandas as pd

# create the data frame from csv file
df = pd.read_csv('pandasLesson3.csv')
print(df.head())

# set the index
df.set_index('Date', inplace=True)
print(df.head())

# dump the data frame to csv file
df.to_csv('pandasLesson3_2.csv')

df = pd.read_csv('pandasLesson3_2.csv')
print(df.head())

# set the column index when load the csv file
df = pd.read_csv('pandasLesson3_2.csv', index_col=0)
print(df.head())

# set the new column name
df.columns = ['HSI Index']
print(df.head())
df.to_csv('pandasLesson3_3.csv')

# it also can disable the header
df.to_csv('pandasLesson3_4.csv', header=False)

# read the csv file and create the column yourself
df = pd.read_csv('pandasLesson3_4.csv', names=['Date','SSC Index'], index_col=0)
print(df.head())

# dump to html table
df.to_html('pandasLesson3.html')


df.rename(columns={'SSC Index':'New Index'}, inplace=True)
print(df.head())

