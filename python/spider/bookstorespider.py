import requests
from bs4 import BeautifulSoup

# 'https://www.books.com.tw/web/sys_newtopb/books/'
homeurl = 'https://www.books.com.tw/web/sys_newtopb/books/'

html = requests.get(homeurl).text
soup = BeautifulSoup(html, 'html.parser')

res = soup.find('div',{'class':'mod type02_m035 clearfix'})
items = res.select(".item")

for item in items:
    msg = item.select('.type02_bd-a')[0]
    title = msg.select('a')[0].text
    author = msg.select('a')[1].text
    print(msg)
    print('Title:' + title)
    print('Author' + author)
    break
