# lesson 6 - date frame joining and merging

import pandas as pd

df1 = pd.DataFrame({'HPI':[80,85,88,85],
                    'Int_rate':[2, 3, 2, 2],
                    'US_GDP_Thousands':[50, 55, 65, 55]},
                   index = [2001, 2002, 2003, 2004])

df2 = pd.DataFrame({'HPI':[80,85,88,85],
                    'Int_rate':[2, 3, 2, 2],
                    'US_GDP_Thousands':[50, 55, 65, 55]},
                   index = [2005, 2006, 2007, 2008])

df3 = pd.DataFrame({'HPI':[80,85,88,85],
                    'Unemployment':[7, 8, 9, 6],
                    'Low_tier_HPI':[50, 52, 50, 53]},
                   index = [2001, 2002, 2003, 2004])


# merging, let merge df1 and df2
print(pd.merge(df1, df2, on='HPI'))
print(pd.merge(df1, df2, on=['HPI','Int_rate']))

# join, and get data duplicate
df1.set_index('HPI', inplace=True)
df3.set_index('HPI', inplace=True)
joined = df1.join(df3)
print(joined)


df1 = pd.DataFrame({'Year':[2001, 2002, 2003, 2004],
                    'Int_rate':[2, 3, 2, 2],
                    'US_GDP_Thousands':[50, 55, 65, 55]})

df3 = pd.DataFrame({'Year':[2001, 2003, 2004, 2005],
                    'Unemployment':[7, 8, 9, 6],
                    'Low_tier_HPI':[50, 52, 50, 53]})

# so merge the inner set year on
merged = pd.merge(df1, df3, on = 'Year')
merged.set_index('Year', inplace = True)
print(merged)

# set how = 'left', it show all year in left side - df1
merged = pd.merge(df1, df3, on = 'Year', how = 'left')
merged.set_index('Year', inplace = True)
print(merged)

# set how = 'right', it show all year in left side - df3
merged = pd.merge(df1, df3, on = 'Year', how = 'right')
merged.set_index('Year', inplace = True)
print(merged)

# set how = 'outer', it show all year in both left side and right side
merged = pd.merge(df1, df3, on = 'Year', how = 'outer')
merged.set_index('Year', inplace = True)
print(merged)

# set how = 'inner', it show all year in both left side and right side
merged = pd.merge(df1, df3, on = 'Year', how = 'inner')
merged.set_index('Year', inplace = True)
print(merged)
