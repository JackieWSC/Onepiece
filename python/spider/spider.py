import requests
from bs4 import BeautifulSoup


def get_header():
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9,zh-TW;q=0.8,zh;q=0.7",
        "Cache-Control": "max-age=0",
        "Referer": "https://www.google.com.hk/",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
    }

    return headers


def get_payload():
    payload = {
        'key1': 'value1'
    }

    return payload


def get_session_payload():
    payload = {
        'from': 'https://www.ptt.cc/ask/over18',
        'yes': 'yes'
    }

    return payload

url = 'http://www.e-happy.com.tw'
html = requests.get(url)
html.encoding = "utf-8"

# if html .status_code == requests.codes.ok:
#    print(html.text)

## Test Get
url = 'http://httpbin.org/get'
headers = get_header()
html = requests.get(url, headers = headers)
html.encoding = "utf-8"

# if html .status_code == requests.codes.ok:
#     print(html.text)

## Test Post
url = 'http://httpbin.org/post'
payload = get_payload()
html = requests.post(url, data=payload)

# if html.status_code == requests.codes.ok:
#     print(html.text)

## Test Session
url = 'https://www.ptt.cc/ask/over18'
headers = get_header()
payload = get_session_payload()
html = requests.post(url, data=payload, headers=headers)

# if html.status_code == requests.codes.ok:
#     print(html.text)

url = 'https://www.ptt.cc/bbs/Gossiping/index.html'
headers = get_header()
html = requests.get(url, headers=headers)
# if html.status_code == requests.codes.ok:
#     print(html.text)

## Test BeautifulSoup

url = 'http://www.e-happy.com.tw'
html = requests.get(url)
sp = BeautifulSoup(html.text, 'html.parser')
print(sp.title)
print(sp.find('h2'))
for a in sp.find_all('a'):
    print(a)

