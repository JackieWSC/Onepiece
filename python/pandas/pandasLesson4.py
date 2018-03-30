# Lesson 4 - quandl api and get the table on html
# It requires quandl, so use to install it first
#   - pip3 install quandl
#   - pip3 install lxml
#   - pip3 install html5lib
# create account on quandl, so you able to use the data in lesson.
# we are going to use house price index with the quandl and
# api key after create the account, so you don't need to download the csv
# manual by hand
#
# Q&A
# <urlopen error [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed (_ssl.c:777)>
# Click Applications => Python then double-click Install Certificates.command.

import quandl
import pandas as pd

# load a api key from file
api_key = open('quandlapikey.txt','r').read()

# get the data of House Price Index - Alaska
df = quandl.get('FMAC/HPI_AK',authtoken=api_key)
print(df.head())

# get the US states table from wiki
# instead od us regex, beautiful soup, it will use the pandas here
fiddy_states = pd.read_html('https://simple.wikipedia.org/wiki/List_of_U.S._states')

# fiddy_states will be a list of table
# this is a list
# print(fiddy_states)

# this is a data frame, so what we need here is the first table
# print(fiddy_states[0])

# this is a second column and what abbreviation we need
print(fiddy_states[0][1])

for abbv in fiddy_states[0][1][1:]:
    print("FMAC/HPI_" + str(abbv))

# so we have a list to get all of the house index by us states
# next: we are going concate and combin the data frame 





