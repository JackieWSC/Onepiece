# lesson 7 - resume what lesson 4 do to analysis real estate with Quandl
# And learn pickle to save any python object instead of save/load from csv
# as it take around 30 seconds to join all of the dataframe
# so we use pickle to save the dataframe to file instead of
# waiting 30 seconds to get back those data from quandl
# pickle able to save all of the python object to file and load back
#
# pandas has it own pickle version which just need one line code to save to file and
# one line code to load from file

import quandl
import pandas as pd
import pickle

# Not necessary, I just do this so I do not show my API key.
api_key = open('quandlapikey.txt','r').read()

def dump_to_pickle_python_version(dataframe):
    pickle_out = open('fiddy_states.pickle','wb')
    pickle.dump(dataframe, pickle_out)
    pickle_out.close()
    
def load_from_pickle_python_version():
    print("load_from_pickle_python_version")
    pickle_in = open('fiddy_states.pickle','rb')
    HPI_data = pickle.load(pickle_in)
    print(HPI_data.head())

def load_from_pickle_pandas_version():
    print("load_from_pickle_pandas_version")
    HPI_data = pd.read_pickle('dataframe.pickle')
    print(HPI_data.head())

def state_list():
    fiddy_states = pd.read_html('https://simple.wikipedia.org/wiki/List_of_U.S._states')    
    return fiddy_states[0][1][1:]


def grab_initial_state_data():
    states = state_list()
    main_df = pd.DataFrame()
    
    for abbv in states:
        query = "FMAC/HPI_" + str(abbv)
        #print(query)
        df = quandl.get(query, authtoken=api_key)
        df.columns = [str(abbv)]

        if main_df.empty:
            main_df = df
        else:
            main_df = main_df.join(df)

    print(main_df.head())

    # so we use pickle to save the dataframe to file instead of
    # waiting 30 seconds to get back those data from quandl
    dump_to_pickle_python_version(main_df)

    # or
    main_df.to_pickle('dataframe.pickle')
    

def sample():
    df1 = quandl.get("FMAC/HPI_AL", authtoken=api_key)
    df2 = quandl.get("FMAC/HPI_AK", authtoken=api_key)

    df1.columns = ['HPI_AL']
    df2.columns = ['HPI_AK']

    print(df1.head())
    print(df2.head())

    joined = df1.join(df2)
    print(joined.head())


#sample()
#grab_initial_state_data()
load_from_pickle_python_version()
load_from_pickle_pandas_version()


