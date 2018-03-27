# lesson 2
# - Pandas Dataframe
# - Know the concept of Index, Column

import pandas as pd
import numpy as np

web_stats = {'Day' : [1,2,3,4,5,6],
             'visitors' : [23,12,23,56,43,33],
             'Rate':[65,87,65,21,34,54]}
df = pd.DataFrame(web_stats)

# print out data frame
##print(df)
##print(df.head())
##print(df.tail())
##print(df.tail(2))

# set index
##print(df.set_index('Day'))
##print(df.set_index('Day', inplace=True))

# print one column
##print(df["visitors"])
##print(df.visitors)

# print two column
##print(df[["Day","visitors"]])

# print visitor list
print("List:", df.visitors.tolist())
print(np.array(df[["Day","visitors"]]))

# convert np array to data frame
df2 = pd.DataFrame(np.array(df[["Day","visitors"]]))
print(df2)
