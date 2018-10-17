import random
import string
import pandas as pd
import numpy as np
np.random.seed(0)

# This is the total number of groups to be created
NumberOfGroups = 50000

# Create a lot of groups (random strings of 4 letters)
Group1     = [''.join(random.choice(string.ascii_uppercase) for _ in range(4)) for x in range(int(NumberOfGroups/10))]*10
Group2     = [''.join(random.choice(string.ascii_uppercase) for _ in range(4)) for x in range(int(NumberOfGroups/2))]*2
FinalGroup = [''.join(random.choice(string.ascii_uppercase) for _ in range(4)) for x in range(int(NumberOfGroups))]

# Make the numbers
NumbersForPercents = [np.random.randint(100, 999) for _ in range(NumberOfGroups)]

# Make the dataframe
df = pd.DataFrame({'Group 1': Group1,
                   'Group 2': Group2,
                   'Final Group': FinalGroup,
                   'Numbers I want as percents': NumbersForPercents})

print(df.head(10).to_string())

# Initial grouping (basically a sorted version of df)
PreGroupby_df = df.groupby(["Group 1","Group 2","Final Group"]).agg({'Numbers I want as percents': 'sum'}).reset_index()
# Get the sum of values for the "final group", append "_Sum" to it's column name, and change it into a dataframe (.reset_index)
SumGroup_df = df.groupby(["Group 1","Group 2"]).agg({'Numbers I want as percents': 'sum'}).add_suffix('_Sum').reset_index()
# Merge the two dataframes
Percents_df = pd.merge(PreGroupby_df, SumGroup_df)
# Divide the two columns
Percents_df["Percent of Final Group"] = Percents_df["Numbers I want as percents"] / Percents_df["Numbers I want as percents_Sum"] * 100
# Drop the extra _Sum column
Percents_df.drop(["Numbers I want as percents_Sum"], inplace=True, axis=1)

print(Percents_df.head(10).to_string())