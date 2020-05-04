import time
import re
from django.shortcuts import render
from django.http import HttpResponse
from stocksapi.models import Visitor
from stocksapi.stocker import Stocker
from stocksapi.utilities import Logger, get_line_number

stocker = Stocker()


# helper - Return True if the request comes from a mobile device.
def mobile(request):

    MOBILE_AGENT_RE = re.compile(r".*(iphone|mobile|androidtouch)", re.IGNORECASE)

    if MOBILE_AGENT_RE.match(request.META['HTTP_USER_AGENT']):
        return True
    else:
        return False


def get_from_cookie(request, function_name, stock_code, load_from_cookie=True):
    create_session_data = False
    json = {}

    if load_from_cookie:
        if function_name in request.session:
            Logger.log_trace('Info', 'check_cookie', get_line_number(),
                             'Found {} session file in Request'.format(function_name))
            kd_index_json_map = request.session[function_name]

            if stock_code in kd_index_json_map:
                json = kd_index_json_map[stock_code]
            else:
                create_session_data = True

        else:
            create_session_data = True

    else:
        create_session_data = True

    return create_session_data, json


def save_to_cookie(request, function_name, stock_code, json):
    json_map = {stock_code: json}
    request.session[function_name] = json_map
    request.session.set_expiry(300)


def check_latency(page_name, start_time):
    latency_ms = (time.time() - start_time) * 1000
    visitor = Visitor(page=page_name, latency=latency_ms)
    visitor.save()

    log = "Latency for {0}: {1}".format(page_name, format(latency_ms, '.2f'))
    Logger.log_trace('Info', 'check_latency', get_line_number(), log)


# Main View Page
def stock_kd(request, stock_code="2800.HK"):
    stock_name = stocker.get_stock_name(stock_code)
    context = {
        'stock_name': stock_name,
        'stock_code': stock_code
    }

    return render(request, "stock.html", context)


def stock_history(request, stock_code="2800.HK"):
    stock_name = stocker.get_stock_name(stock_code)
    context = {
        'stock_name': stock_name,
        'stock_code': stock_code
    }

    return render(request, "stockhistory.html", context)


def backtesting(request, stock_code="2800.HK"):
    stock_name = stocker.get_stock_name(stock_code)
    is_mobile = mobile(request)
    context = dict(stock_name=stock_name, stock_code=stock_code, is_mobile=is_mobile)

    return render(request, "backtesting.html", context)


def playground(request):
    start_time = time.time()

    send_to_line = False
    stocker.get_stock_list_kd(send_to_line)

    # calculate the latency
    check_latency('playground', start_time)

    return render(request, "playground.html")


def checker(request, stock_code="2800.HK", year=2018):
    stock_name = stocker.get_stock_name(stock_code)
    context = dict(stock_name=stock_name, stock_code=stock_code, year=year)

    return render(request, "checker.html", context)


def main(request):
    stock_list = ["^HSI",
                  "2800.HK",
                  "0700.HK",
                  "2822.HK",
                  "2834.HK",
                  "1810.HK",
                  "0175.HK"]

    stock_count = len(stock_list)

    context = {
        'stock_list': stock_list,
        'stock_count': stock_count
    }

    return render(request, "main.html", context)

# Line Notification


# Call by IFTTT and send the message to LINE API
def check_next_kd_index(request, stock_code="2800.HK"):
    start_time = time.time()

    # main function
    send_to_line = True
    stocker.create_next_kd_index(stock_code, send_to_line)

    # calculate the latency
    check_latency('check_next_kd_index', start_time)

    return render(request, "index.html")


def check_stock_list_kd_index(request):
    start_time = time.time()

    # main function
    send_to_line = True
    stocker.get_stock_list_kd(send_to_line)

    # calculate the latency
    check_latency('check_stock_list_kd_index', start_time)

    return render(request, "index.html")


def daily_update_jobs(request):
    start_time = time.time()

    # main function
    save_to_db = True
    stocker.create_last_api_data_to_db(save_to_db)
    stocker.create_last_kd_data_to_db(save_to_db)

    # calculate the latency
    check_latency('check_stock_list_kd_index', start_time)

    return render(request, "index.html")

# RESTFUL API interface


# Get the price history by stock code
# It can get the 1, 3 and 10 years data
def get_stock_price_history(request, stock_code="2800.HK", year=10):
    print(stock_code, year)

    start_time = time.time()

    # main function
    json = stocker.create_stock_price_history(stock_code, year)

    # calculate the latency
    check_latency('stock_price_history', start_time)

    return HttpResponse(json)


# Get the KD index in last 20 trading date
def get_kd_index(request, stock_code="2800.HK"):
    start_time = time.time()

    # main function
    create_session_data, json = get_from_cookie(request, 'kd_index_json', stock_code, False)

    if create_session_data:
        Logger.log_trace('Info', 'get_kd_index', get_line_number(),
                         'Create kd_index_json session file to Request')
        json = stocker.create_kd_index(stock_code)

        # add to cookies
        save_to_cookie(request, 'kd_index_json', stock_code, json)

    # calculate the latency
    check_latency('get_kd_index', start_time)

    return HttpResponse(json)


# Get the KD index of next trading date
def get_next_kd_index(request, stock_code="2800.HK"):
    start_time = time.time()

    # main function
    create_session_data, json = get_from_cookie(request, 'next_kd_index_json', stock_code, False)

    if create_session_data:
        Logger.log_trace('Info', 'get_next_kd_index', get_line_number(),
                         'Found next_kd_index_json session file in Request')
        json = stocker.create_next_kd_index(stock_code)

        # add to cookies
        save_to_cookie(request, 'next_kd_index_json', stock_code, json)

    # calculate the latency
    check_latency('get_next_kd_index', start_time)

    return HttpResponse(json)


def get_db_data(request, stock_code="2800.HK", year=2018):
    start_time = time.time()

    # main function
    json = stocker.get_db_data(stock_code, year)

    # calculate the latency
    check_latency('get_db_data', start_time)

    return HttpResponse(json)


def get_db_kd_data(request, stock_code="2800.HK", year=2018):
    start_time = time.time()

    # main function
    json = stocker.get_db_kd_data(stock_code, year)

    # calculate the latency
    check_latency('get_db_kd_data', start_time)

    return HttpResponse(json)


def create_api_data_to_db(request, stock_code="2800.HK", year=2018, input_type="default"):
    start_time = time.time()

    # main function
    json = stocker.create_api_data_to_db(stock_code, year, input_type)

    # calculate the latency
    check_latency('create_db_from_api_data', start_time)

    return HttpResponse(json)


def create_kd_data_to_db(request, stock_code="2800.HK", start_date="2019-01-01", input_type="default"):
    start_time = time.time()

    # main function
    json = stocker.create_kd_data_to_db(stock_code, start_date, input_type)

    # calculate the latency
    check_latency('create_kd_data_to_db', start_time)

    return HttpResponse(json)


def create_kd_data_to_db_with_api(request, stock_code="2800.HK", input_type="default"):
    start_time = time.time()

    # main function
    json = stocker.create_kd_data_to_db_with_api_data(stock_code, input_type)

    # calculate the latency
    check_latency('create_kd_data_to_db_with_api_data', start_time)

    return HttpResponse(json)
