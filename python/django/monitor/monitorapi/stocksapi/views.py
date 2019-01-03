import time
from django.shortcuts import render
from django.http import HttpResponse
from stocksapi.models import Visitor
from stocksapi.stocker import Stocker
from stocksapi.utilities import Logger, get_line_number

stocker = Stocker()


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


def playground(request):
    return render(request, "playground.html")


def checker(request, stock_code="2800.HK"):
    stock_name = stocker.get_stock_name(stock_code)
    context = dict(stock_name=stock_name, stock_code=stock_code)

    return render(request, "checker.html", context)

# Line Notification


# Call by IFTTT and send the message to LINE API
def check_next_kd_index(request, stock_code="2800.HK"):
    start_time = time.time()

    # main function
    send_to_line = True
    stocker.create_next_kd_index(stock_code, send_to_line)

    # calculate the latency
    latency_ms = (time.time() - start_time) * 1000
    visitor = Visitor(page='check_next_kd_index', latency=latency_ms)
    visitor.save()

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
    latency_ms = (time.time() - start_time) * 1000
    visitor = Visitor(page='stock_price_history', latency=latency_ms)
    visitor.save()

    return HttpResponse(json)


# Get the KD index in last 20 trading date
def get_kd_index(request, stock_code="2800.HK"):
    start_time = time.time()

    # main function
    kd_index_json_map = {}
    create_session_data = False
    if 'kd_index_json' in request.session:
        Logger.log_trace('Info', 'get_kd_index', get_line_number(),
                         'Found kd_index_json session file in Request')
        kd_index_json_map = request.session['kd_index_json']

        if stock_code in kd_index_json_map:
            json = kd_index_json_map[stock_code]
        else:
            create_session_data = True

    else:
        create_session_data = True

    if create_session_data:
        Logger.log_trace('Info', 'get_kd_index', get_line_number(),
                         'Create kd_index_json session file to Request')
        json = stocker.create_kd_index(stock_code)
        kd_index_json_map[stock_code] = json
        request.session['kd_index_json'] = kd_index_json_map
        request.session.set_expiry(300)

    # calculate the latency
    latency_ms = (time.time() - start_time) * 1000
    visitor = Visitor(page='kd_index', latency=latency_ms)
    visitor.save()

    log = "Latency: {0}".format(format(latency_ms, '.2f'))
    Logger.log_trace('Info', 'get_kd_index', get_line_number(), log)

    return HttpResponse(json)


# Get the KD index of next trading date
def get_next_kd_index(request, stock_code="2800.HK"):
    start_time = time.time()

    # main function
    next_kd_index_json_map = {}
    create_session_data = False
    if 'next_kd_index_json' in request.session:
        Logger.log_trace('Info', 'next_kd_index_json', get_line_number(),
                         'Found next_kd_index_json session file in Request')
        next_kd_index_json_map = request.session['next_kd_index_json']

        if stock_code in next_kd_index_json_map:
            json = next_kd_index_json_map[stock_code]
        else:
            create_session_data = True

    else:
        create_session_data = True

    if create_session_data:
        Logger.log_trace('Info', 'next_kd_index_json', get_line_number(),
                         'Create next_kd_index_json session file to Request')
        json = stocker.create_next_kd_index(stock_code)
        next_kd_index_json_map[stock_code] = json
        request.session['next_kd_index_json'] = next_kd_index_json_map
        request.session.set_expiry(300)

    # calculate the latency
    latency_ms = (time.time() - start_time) * 1000
    visitor = Visitor(page='next_kd_index', latency=latency_ms)
    visitor.save()

    log = "Latency: {0}".format(format(latency_ms, '.2f'))
    Logger.log_trace('Info', 'get_next_kd_index', get_line_number(), log)

    return HttpResponse(json)


def get_db_data(request, stock_code="2800.hk"):
    start_time = time.time()

    # main function
    json = stocker.get_db_data(stock_code)

    # calculate the latency
    latency_ms = (time.time() - start_time) * 1000
    visitor = Visitor(page='get_db_data', latency=latency_ms)
    visitor.save()

    log = "Latency: {0}".format(format(latency_ms, '.2f'))
    Logger.log_trace('Info', 'get_db_data', get_line_number(), log)

    return HttpResponse(json)


def get_db_kd_data(request, stock_code="2800.hk"):
    start_time = time.time()

    # main function
    json = stocker.get_db_kd_data(stock_code)

    # calculate the latency
    latency_ms = (time.time() - start_time) * 1000
    visitor = Visitor(page='get_db_kd_data', latency=latency_ms)
    visitor.save()

    log = "Latency: {0}".format(format(latency_ms, '.2f'))
    Logger.log_trace('Info', 'get_db_kd_data', get_line_number(), log)

    return HttpResponse(json)


def create_api_data_to_db(request, stock_code="2800.hk"):
    start_time = time.time()

    # main function
    json = stocker.create_api_data_to_db(stock_code)

    # calculate the latency
    latency_ms = (time.time() - start_time) * 1000
    visitor = Visitor(page='create_db_from_api_data', latency=latency_ms)
    visitor.save()

    log = "Latency: {0}".format(format(latency_ms, '.2f'))
    Logger.log_trace('Info', 'create_db_from_api_data', get_line_number(), log)

    return HttpResponse(json)


def create_kd_data_to_db(request, stock_code="2800.hk"):
    start_time = time.time()

    # main function
    json = stocker.create_kd_data_to_db(stock_code)

    # calculate the latency
    latency_ms = (time.time() - start_time) * 1000
    visitor = Visitor(page='create_kd_data_to_db', latency=latency_ms)
    visitor.save()

    log = "Latency: {0}".format(format(latency_ms, '.2f'))
    Logger.log_trace('Info', 'create_kd_data_to_db', get_line_number(), log)

    return HttpResponse(json)
