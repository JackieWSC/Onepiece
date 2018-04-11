# lesson 7 - resume what lesson 4 do to analysis real estate with Quandl
# And learn pickle to save any python object instead of save/load from csv
import quandl
import pandas as pd

# Not necessary, I just do this so I do not show my API key.
api_key = open('quandlapikey.txt','r').read()
fiddy_states = pd.read_html('https://simple.wikipedia.org/wiki/List_of_U.S._states')

df1 = quandl.get("FMAC/HPI_AL", authtoken=api_key)
df2 = quandl.get("FMAC/HPI_AK", authtoken=api_key)

df1.columns = ['HPI_AL']
df2.columns = ['HPI_AK']

print(df1.head())
print(df2.head())

joined = df1.join(df2)
print(joined.head())

main_df = pd.DataFrame()
for abbv in fiddy_states[0][1][1:]:
    #print(abbv)
    #print("FMAC/HPI_" + str(abbv))
    query = "FMAC/HPI_" + str(abbv)
    #print(query)
    df = quandl.get(query, authtoken=api_key)

    df.columns = [str(abbv)]

    if main_df.empty:
        main_df = df
    else:
        main_df = main_df.join(df)

print(main_df.head())
