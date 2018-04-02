# lesson 5 - concatenation, appending dataframes
# for different dataframes, we may need to share the index, or column
# concat and append are the method what we can manipulate
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
                    'Int_rate':[2, 3, 2, 2],
                    'Low_tier_HPI':[50, 52, 50, 53]},
                   index = [2001, 2002, 2003, 2004])

# df1 and df3 have same index (2001 to 2004), but different columns
# df1 and df2 have same columns and different index

# for the concatenation, it concate columns, and the indexs are on sequence
concat = pd.concat([df1, df2])
print(concat)

# if conate df3, there are NaN
concat = pd.concat([df1, df2, df3])
print(concat)

df4 = df1.append(df2)
print(df4)

# they share the same index? no, it is not
df4 = df1.append(df3)
print(df4)

# it will add one row and 3 new columns
s = pd.Series([80, 2, 50])
df4 = df1.append(s, ignore_index = True)
print(df4)

# it will append a new row if defined the column same as df1
s = pd.Series([80, 2, 50], index = ['HPI','Int_rate','US_GDP_Thousands'])
df4 = df1.append(s, ignore_index = True)
print(df4)



