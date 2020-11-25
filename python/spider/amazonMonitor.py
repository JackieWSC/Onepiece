import datetime
import requests
import time
from bs4 import BeautifulSoup
from random import randrange

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


def check_item_in_stock(link):
    # send the requests and use BeautifulSoup to convert the html
    result = False
    message = ''
    resp = requests.get(link)
    html = resp.text
    soup = BeautifulSoup(html, 'lxml')

    if resp.status_code == 200:
        # get the keyword
        availability_feature_div = soup.find('div', {'id': 'availability_feature_div'})
        price = soup.find('div', {'id': 'price'})
        productTitle = soup.find('span', {'id': 'productTitle'})

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
        print('resp.status_code not equal to 200')

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
amazon_urls = [
                'https://www.amazon.co.jp/dp/B07T5V4TCV/',
                'https://www.amazon.co.jp/dp/B077Z999TC/',
                'https://www.amazon.co.jp/dp/B0785VKT85/',
                'https://www.amazon.co.jp/dp/B07YV93GNH/',
                # 'https://www.amazon.co.jp/dp/B081JYCDRP/',
                # 'https://www.amazon.co.jp/dp/B008L3R8BM/',
                'https://www.amazon.co.jp/gp/product/B00FYQCJQI/'
              ]
poll_time = 1
monitor_time = 60

# start
while True:
    print('\n {} Start Checking!!'.format(datetime.datetime.now()))
    for link in amazon_urls:
        print('\n--------------------------------------------------')

        result, message = check_item_in_stock(link)
        if result:
            print('\nSend the Line Notification')
            notification(message)

        time.sleep(poll_time)
        print('--------------------------------------------------')

    print('\nWait for next monitor time!!')
    next_monitor_time = monitor_time + randrange(10)
    time.sleep(next_monitor_time)

print('\n End Program!!')
