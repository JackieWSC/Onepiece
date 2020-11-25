# -*- coding: utf-8 -*-
"""
Examples for use the python functions: get push data
"""
from time import sleep
from futu import *


class SysNotifyTest(SysNotifyHandlerBase):
    def on_recv_rsp(self, rsp_pb):
        """数据响应回调函数"""
        ret_code, content = super(SysNotifyTest, self).on_recv_rsp(rsp_pb)
        notify_type, sub_type, msg = content
        if ret_code != RET_OK:
            logger.debug("SysNotifyTest: error, msg: %s" % content)
            return RET_ERROR, content
        else:
            print('* SysNotifyTest: msg:{}'.format(msg))
        return RET_OK, content

# output example:
#
# * StockQuoteTest: ret_code:0
#         code   data_date data_time  last_price  open_price  high_price  low_price  prev_close_price       volume      turnover  turnover_rate  amplitude  suspension listing_date  price_spread dark_status  strike_price  contract_size  open_interest  implied_volatility  premium  delta  gamma  vega  theta  rho
# 0  SH.000001  2020-03-04  13:09:58   2987.8267    2981.806   3001.5594  2980.2033         2992.8968  20596198400  2.290515e+11            0.0      0.714       False   1970-01-01          0.01         N/A           0.0              0              0                 0.0      0.0    0.0    0.0   0.0    0.0  0.0
#
# [1 rows x 26 columns]
class StockQuoteTest(StockQuoteHandlerBase):
    """
    获得报价推送数据
    """
    def on_recv_rsp(self, rsp_pb):
        """数据响应回调函数"""
        ret_code, content = super(StockQuoteTest, self).on_recv_rsp(rsp_pb)
        if ret_code != RET_OK:
            logger.debug("StockQuoteTest: error, msg: %s" % content)
            return RET_ERROR, content
        else:
            print('* StockQuoteTest: ret_code:{}'.format(ret_code))
            print(content)
        return RET_OK, content


class TickerTest(TickerHandlerBase):
    """ 获取逐笔推送数据 """
    def on_recv_rsp(self, rsp_pb):
        """数据响应回调函数"""
        ret_code, content = super(TickerTest, self).on_recv_rsp(rsp_pb)
        if ret_code != RET_OK:
            print("* TickerTest: error, msg: %s" % content)
            return RET_ERROR, content
        else:
            print('* TickerTest: ret_code:{}, content:{}'.format(ret_code, content))
        return RET_OK, content


class OrderBookTest(OrderBookHandlerBase):
    """ 获得摆盘推送数据 """
    def on_recv_rsp(self, rsp_pb):
        """数据响应回调函数"""
        ret_code, content = super(OrderBookTest, self).on_recv_rsp(rsp_pb)
        if ret_code != RET_OK:
            print("* OrderBookTest: error, msg: %s" % content)
            return RET_ERROR, content
        else:
            print('* OrderBookTest: ret_code:{}, content:{}'.format(ret_code, content))
        return RET_OK, content


class BrokerTest(BrokerHandlerBase):
    """ 获取经纪队列推送数据 """
    def on_recv_rsp(self, rsp_pb):
        """数据响应回调函数"""
        ret_code, stock_code, contents = super(BrokerTest, self).on_recv_rsp(rsp_pb)
        if ret_code != RET_OK:
            print("* BrokerTest: error, msg: %s" % contents)
            return RET_ERROR, contents
        else:
            print('* BrokerTest: ret_code:{}, content:{}'.format(ret_code, contents))
        return ret_code


#
# * RTDataTest: ret_code:0, content:        code                 time  is_blank  opened_mins  cur_price  last_close    avg_price  turnover  volume
# 0  SH.000001  2020-03-04 13:11:00     False          791  2987.8267   2992.8968  2992.268345       0.0       0
#
class RTDataTest(RTDataHandlerBase):

    def on_recv_rsp(self, rsp_pb):
        """数据响应回调函数"""
        ret_code, contents = super(RTDataTest, self).on_recv_rsp(rsp_pb)
        if ret_code != RET_OK:
            print("* RTDataTest: error, msg: %s" % contents)
            return RET_ERROR, contents
        else:
            print('* RTDataTest: ret_code:{}, content:{}'.format(ret_code, contents))
        return ret_code


def quote_test():
    '''
    行情接口调用测试
    :return:
    '''
    quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)

    # setup async callback interface
    quote_ctx.start()
    quote_ctx.set_handler(SysNotifyTest())
    quote_ctx.set_handler(StockQuoteTest())
    quote_ctx.set_handler(TickerTest())
    quote_ctx.set_handler(OrderBookTest())
    quote_ctx.set_handler(BrokerTest())
    quote_ctx.set_handler(RTDataTest())

    # acquire pushing data
    big_sub_codes = ['HK.02318', 'HK.02828', 'HK.00939', 'HK.01093', 'HK.01299', 'HK.00175',
                     'HK.01299', 'HK.01833', 'HK.00005', 'HK.00883', 'HK.00388', 'HK.01398',
                     'HK.01114', 'HK.02800', 'HK.02018', 'HK.03988', 'HK.00386', 'HK.01211',
                     'HK.00700', 'HK.01177',  'HK.02601', 'HK.02628', 'HK_FUTURE.999010']
    # subtype_list = [SubType.QUOTE, SubType.ORDER_BOOK, SubType.TICKER, SubType.BROKER, SubType.RT_DATA]
    subtype_list = [SubType.QUOTE, SubType.RT_DATA]
    # sub_codes = ['HK.00700', 'HK_FUTURE.999010']
    sub_codes = ['SH.000001']

    # subscribe data
    print("* subscribe : {}\n".format(quote_ctx.subscribe(sub_codes, subtype_list)))

    # loop
    while True:
        # Wait for handler callback
        print("* query_subscription : {}\n".format(quote_ctx.query_subscription(True)))
        print('* Sleep..')
        sleep(61)

    quote_ctx.close()


# use the futu api to subscript the market data
#   the market data will be pushing by server
if __name__ == "__main__":
    set_futu_debug_model(True)

    # pandas setup
    pd.set_option('display.max_columns', 100)
    pd.set_option('display.width', 1000)

    ''' 行情api测试 '''
    # SH.000001 success
    # hk stock need level 2 right
    # us keep empty list
    quote_test()
