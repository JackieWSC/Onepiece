import datetime
import requests
import time
from bs4 import BeautifulSoup
from random import randrange
import requests.packages.urllib3

# define the items list which need to monitor
# loop the items in list to send the request to amazon
#   - if the item is out of store, print the
#     - description
#     - title
#   - if the item is available, print the
#     - description
#     - Title
#     - Price
#     - Link


# check the amazon stock
def check_item_in_amazon_stock(headers, link):
    # send the requests and use BeautifulSoup to convert the html
    result = False
    message = ''
    session = requests.Session()
    resp = session.get(link, headers=headers, allow_redirects=True, verify=False)
    html = resp.text
    soup = BeautifulSoup(html, 'lxml')

    if resp.status_code == 200:
        # get the keyword
        availability_feature_div = soup.find('div', {'id': 'availability_feature_div'})
        price = soup.find('div', {'id': 'price'})
        productTitle = soup.find('span', {'id': 'productTitle'})
        item_price = ''
        item_title = ''

        if price and price.find('span', {'id': 'priceblock_ourprice'}):
            item_price = price.find('span', {'id': 'priceblock_ourprice'}).get_text().strip()
            # print(item_price)

        if productTitle:
            item_title = productTitle.get_text().strip()
            # print(productTitle)

        # check if the item is available
        #   - if the item is not available, the <span> can be found
        if availability_feature_div:

            availability = availability_feature_div.find('span')
            if availability:
                message += 'Out of stock:[{}]\n'.format(availability.get_text().strip())
                message += 'Title:[{}]\n'.format(item_title)
                message += 'Link:[{}]\n'.format(link)
                print(message)
            else:
                message += 'Item Available!\n'
                message += 'Title:[{}]\n'.format(item_title)
                message += 'Price:[{}]\n'.format(item_price)
                message += 'Link:[{}]\n'.format(link)
                result = True
                print(message)
        else:
            print('Can not find id=availability_feature_div')
            print('Link:[{}]'.format(link))
    else:
        print('resp.status_code [{}] not equal to 200'.format(resp.status_code))
        print('Link:[{}]'.format(link))

    return result, message


# check the hktv mall stock
def check_item_in_hktv_stock(headers, link):
    # send the requests and use BeautifulSoup to convert the html
    result = False
    message = ''
    try:
        session = requests.Session()
        resp = session.get(link, headers=headers, allow_redirects=True, verify=False)
    except requests.exceptions.RequestException as e:
        print(e)
        return result, message

    html = resp.text
    soup = BeautifulSoup(html, 'lxml')

    if resp.status_code == 200:
        # get the keyword
        app_error = soup.find('meta', {'name': 'hktv_app_error_zh'})
        availability = soup.find('div', {'class': 'stockLevelMsg1'})
        price = soup.find('div', {'class': 'price'})
        productTitle = soup.find('h1', {'class': 'last'})
        item_price = ''
        item_title = ''

        if price and price.find('span'):
            item_price = price.find('span').get_text().strip()
            # print(item_price)

        if productTitle:
            item_title = productTitle.get_text().strip()
            # print(productTitle)

        if item_price != '' and item_title != '':
            # check if the item is available
            if availability:
                message += 'Out of stock:[{}]\n'.format(availability.find('span').get_text().strip())
                message += 'Title:[{}]\n'.format(item_title)
                message += 'Link:[{}]\n'.format(link)
                print(message)
            else:
                message += 'Item Available!\n'
                message += 'Title:[{}]\n'.format(item_title)
                message += 'Price:[{}]\n'.format(item_price)
                message += 'Link:[{}]\n'.format(link)
                result = True
                print(message)
        else:
            print('Can not read the Title and Price')
            print('Title:[{}]'.format(item_price))
            print('Price:[{}]'.format(item_title))
            print('Link:[{}]'.format(link))
            print(app_error)

    else:
        print('resp.status_code [{}] not equal to 200'.format(resp.status_code))
        print('Link:[{}]'.format(link))

    return result, message


def notification(text):
    # define the webhooks
    IFTTT_WEBHOOKS_URL = 'https://maker.ifttt.com/trigger/{}/with/key/{}'
    event = 'amazon_monitor'
    token = 'jSfmLiQN7-TxzISuY3kE6p-gusxDr3CTivpaHqNWFCG'
    url_ifttt = IFTTT_WEBHOOKS_URL.format(event, token)
    print('IFTTT URL:{0}'.format(url_ifttt))

    # define the payload
    data = {
        'value1': text
    }

    # send the request to ifttt
    req = requests.post(url_ifttt, data)
    print('Request Text:{0}'.format(req.text))


# main call


# config
monitor_amazon = False
amazon_urls = [
                'https://www.amazon.co.jp/dp/B07T5V4TCV/', # smaller size
                'https://www.amazon.co.jp/dp/B077Z999TC/',
                'https://www.amazon.co.jp/dp/B0785VKT85/', # regular size
                'https://www.amazon.co.jp/dp/B07T3MNKKW/',
                # 'https://www.amazon.co.jp/dp/B07VGCMJTD/ref=asbs_19?_encoding=UTF8&pd_rd_i=B07VGCMJTD&pd_rd_r=6ea6c5f7-a7f6-4306-9035-f1996cc069ec&pd_rd_w=3KIa3&pd_rd_wg=gdUKI&pf_rd_p=ae9d2419-161a-4c59-9424-b1a70d7ddea1&pf_rd_r=KRPDMWGWSW9CMWHJDHA1&ppw=fresh&psc=1',
                # 'https://www.amazon.co.jp/dp/B07VJDJNWS/ref=asbs_2/355-7387708-9204824?_encoding=UTF8&pd_rd_i=B07VJDJNWS&pd_rd_r=063a7ad4-a553-49a1-bbf8-004bc4258736&pd_rd_w=WXiW8&pd_rd_wg=D03rQ&pf_rd_p=ae9d2419-161a-4c59-9424-b1a70d7ddea1&pf_rd_r=ZMZ6XBRFJ6AMF2G8GTWD&ppw=fresh&psc=1',
                # 'https://www.amazon.co.jp/dp/B081JYCDRP/',
                # 'https://www.amazon.co.jp/dp/B008L3R8BM/',
              ]

monitor_hktv = True
hktv_urls = [
                'https://www.hktvmall.com/hktv/zh/main/Sun-Grocery-HK-Limited/s/S1056001/護理保健/護理保健/醫藥產品/口罩/日本高密度PM25大人三層口罩60個裝175X90mm平行進口/p/S1056001_S_8SUNM-001',
                'https://www.hktvmall.com/hktv/zh/main/逸景國際醫療有限公司/s/H6214001/護理保健/護理保健/醫藥產品/口罩/Life-3D手術口罩60片-小童-日本製/p/H6214001_S_H_life3D_S',
                'https://www.hktvmall.com/hktv/zh/main/%E6%BB%B4%E9%9C%B2/s/H1010002/%E8%B6%85%E7%B4%9A%E5%B7%BF%E5%A0%B4/%E8%B6%85%E7%B4%9A%E5%B8%82%E5%A0%B4/%E5%AE%B6%E5%B1%85%E6%B8%85%E6%BD%94%E7%94%A8%E5%93%81/%E6%BC%82%E7%99%BD%E6%B0%B4-%E6%B6%88%E6%AF%92%E5%8A%91/%E5%84%AA%E6%83%A0%E5%AD%96%E8%A3%9D-%E8%90%AC%E7%94%A8%E6%B6%88%E6%AF%92%E5%99%B4%E9%9C%A7/p/H0888001_S_10003163A',
                'https://www.hktvmall.com/hktv/zh/main/%E5%A4%A7%E8%A1%97%E5%B8%82/s/H0888001/%E8%B6%85%E7%B4%9A%E5%B7%BF%E5%A0%B4/%E8%B6%85%E7%B4%9A%E5%B8%82%E5%A0%B4/%E9%86%AB%E8%97%A5%E7%94%A2%E5%93%81/%E5%8F%A3%E7%BD%A9/Level-3-%E5%A4%96%E7%A7%91%E6%89%8B%E8%A1%93%E5%8F%A3%E7%BD%A9-%E4%B8%AD%E7%A2%BC30%E5%80%8B-%E6%AF%8F%E5%80%8B%E5%AE%A2%E6%88%B6%E5%8F%AA%E5%8F%AF%E9%99%90%E8%B3%BC1%E4%BB%B6/p/H0888001_S_10138276',
                'https://www.hktvmall.com/hktv/zh/main/%E5%A4%A7%E8%A1%97%E5%B8%82/s/H0888001/%E8%B6%85%E7%B4%9A%E5%B7%BF%E5%A0%B4/%E8%B6%85%E7%B4%9A%E5%B8%82%E5%A0%B4/%E9%86%AB%E8%97%A5%E7%94%A2%E5%93%81/%E5%8F%A3%E7%BD%A9/Level-3-%E5%A4%96%E7%A7%91%E6%89%8B%E8%A1%93%E5%8F%A3%E7%BD%A9-%E5%A4%A7%E7%A2%BC30%E5%80%8B-%E6%AF%8F%E5%80%8B%E5%AE%A2%E6%88%B6%E5%8F%AA%E5%8F%AF%E9%99%90%E8%B3%BC1%E4%BB%B6/p/H0888001_S_10138275',
                'https://www.hktvmall.com/hktv/zh/main/HE-AMAZING/s/H6646001/%E8%B6%85%E7%B4%9A%E5%B7%BF%E5%A0%B4/%E8%B6%85%E7%B4%9A%E5%B8%82%E5%A0%B4/%E7%B4%99%E5%93%81-%E5%8D%B3%E6%A3%84%E5%93%81-%E5%AE%B6%E5%B1%85%E7%94%A8%E5%93%81/%E6%BF%95%E7%B4%99%E5%B7%BE/%E9%86%AB%E7%94%A8%E4%B8%80%E6%AC%A1%E6%80%A770%E9%85%92%E7%B2%BE%E6%B6%88%E6%AF%92%E6%BF%95%E7%B4%99%E5%B7%BE150%E7%89%8730%E7%9B%92%E8%B6%85%E5%BC%B7%E6%AE%BA%E8%8F%8C%E6%B6%88%E6%AF%92%E6%8A%97%E8%82%BA%E7%82%8E%E9%BD%8A%E4%BE%86%E6%8A%97%E8%82%BA%E7%82%8E%E5%8F%A3%E7%BD%A9%E4%B9%8B%E5%A4%96%E5%87%BA%E9%96%80%E5%AE%B6%E5%B1%85%E8%BE%A6%E5%85%AC%E5%AE%A4%E5%BF%85%E5%82%99/p/H6646001_S_app3',
                # 'https://www.hktvmall.com/hktv/zh/main/3M/s/H0389001/%E7%8E%A9%E5%85%B7%E5%9C%96%E6%9B%B8/%E7%8E%A9%E5%85%B7%E5%9C%96%E6%9B%B8/%E6%96%87%E5%85%B7/%E4%BF%AE%E6%AD%A3%E7%94%A8%E5%93%81/%E6%94%B9%E9%8C%AF%E5%B8%B6/%E6%9B%BF%E6%8F%9B%E5%BC%8F%E6%94%B9%E9%8C%AF%E5%B8%B6%E5%84%AA%E6%83%A0%E8%A3%9D-%E5%85%AD%E6%9B%BF%E8%8A%AF-4%E6%AF%AB%E7%B1%B3-x-10%E7%B1%B3/p/H0389001_S_4891203054428?source=igodigital'
              ]
poll_time = 1
monitor_time = 60

# start
while True:
    requests.packages.urllib3.disable_warnings()

    headers = {
        "User-Agent" 	    : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.4 Safari/605.1.15',
        "Accept"			: "application/xml, text/xml, */*; q=0.01",
        "Accept-Encoding" 	: "gzip, deflate",
        "Accept-Languag"	: "Accept-Language: en,en-US;q=0.8,zh-TW;q=0.6,zh;q=0.4,zh-CN;q=0.2"
    }

    if monitor_amazon:
        print('\n {} Start Checking Amazon !!'.format(datetime.datetime.now()))
        for link in amazon_urls:
            print('\n--------------------------------------------------')

            result, message = check_item_in_amazon_stock(headers, link)
            if result:
                print('\nSend the Line Notification')
                notification(message)

            time.sleep(poll_time)
            print('--------------------------------------------------')

    if monitor_hktv:
        print('\n {} Start Checking HKTV !!'.format(datetime.datetime.now()))
        for link in hktv_urls:
            print('\n--------------------------------------------------')

            result, message = check_item_in_hktv_stock(headers, link)
            if result:
                print('\nSend the Line Notification')
                notification(message)

            time.sleep(poll_time)
            print('--------------------------------------------------')

    print('\nWait for next monitor time!!')
    next_monitor_time = monitor_time + randrange(10)
    time.sleep(next_monitor_time)

print('\n End Program!!')
