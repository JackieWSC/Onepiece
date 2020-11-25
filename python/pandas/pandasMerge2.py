import pandas as pd

df1 = pd.DataFrame(
    {'A': list('ABCA'),
     'B': [1, 2, 3, 4]})

df2 = pd.DataFrame(
    {'C': ['ee', 'bA', 'cCc', 'D'],
     'D': [1, 2, 3, 4]})

print(df1)
print(df2)

temp = set()
for x in df1.A:
    temp.add(x)

pat = '|'.join(r"{}".format(x) for x in temp)
print('\npat:{}'.format(pat))

df2['Test3'] = df2.C.str.extract('(' + pat + ')',
                                 expand=False)
print('\ndf2:\n', df2)

# df2['Test3'] = df2.C.str.extract('(' + pat + ')',
#                                  expand=True)
# print('\ndf2:\n', df2)

result = pd.merge(df1,
                  df2[['D', 'Test3']],
                  left_on='A',
                  right_on='Test3',
                  how='left').drop('Test3', axis=1)

print('\ndf2 left join df1 Result:\n', result)

result = pd.merge(df2,
                  df1,
                  left_on='Test3',
                  right_on='A',
                  how='left').drop(['Test3', 'A'], axis=1)

print('\ndf1 left join df2 Result:\n', result)
