# import futu-api
import futu as ft

# create the stock quote object
quote_ctx = ft.OpenQuoteContext(host="127.0.0.1", port=11111)

# stock quote control
quote_ctx.start()              # open async data receive
quote_ctx.set_handler(ft.TickerHandlerBase())  # setup the handler for async date call back

# low frequency data interface
print('Low Frequency Data Interface \n')
market = ft.Market.US
code = 'HK.02800'
code_list = [code, 'HK.00700']
plate = 'HK.BK1107'
# print('Get the trade date:')
# print(quote_ctx.get_trading_days(market, start=None, end=None))   # get the trade date
print('Get the stock base info:')
print(quote_ctx.get_stock_basicinfo(market, stock_type=ft.SecurityType.STOCK))   # get the stock base info
# print('Get the autype list:')
# print(quote_ctx.get_autype_list(code_list))                                  # 获取复权因子
print('Get market snapshot:')
print(quote_ctx.get_market_snapshot(code_list))                              # get the market snapshot
market_snapshot = quote_ctx.get_market_snapshot(code_list)

# loop the data frame row to dump the data by column name
# for index, row in market_snapshot[1].iterrows():
#     print(row['code'], row['last_price'], row['volume'], row['turnover'])

# print('Get plate list:')
# print(quote_ctx.get_plate_list(market, ft.Plate.ALL))                         # get the plate list
# print('Get plate stock:')
# print(quote_ctx.get_plate_stock(plate))                         # get the stock list by plate code

print('High Frequency Data Interface \n')

code = 'HK.02800'
# high frequency data interface
subscribe_result = quote_ctx.subscribe(code,
                    [ft.SubType.QUOTE,
                     ft.SubType.TICKER,
                     ft.SubType.K_DAY,
                     ft.SubType.ORDER_BOOK,
                     ft.SubType.RT_DATA,
                     ft.SubType.BROKER])

print('Subscribe Result:{0}'.format(subscribe_result))

if subscribe_result[0] != -1:
    print('Get stock quote:')
    print(quote_ctx.get_stock_quote(code))  # get the stock quote
    print('Get tick data:')
    print(quote_ctx.get_rt_ticker(code))   # get tick by tick data
    print('Get kline:')
    print(quote_ctx.get_cur_kline(code, num=10, ktype=ft.KLType.K_DAY))   # get the k value
    print('Get order book:')
    print(quote_ctx.get_order_book(code))       # get the book
    print('Get rt data:')
    print(quote_ctx.get_rt_data(code))          # 获取分时数据
    print('Get broker queue:')
    print(quote_ctx.get_broker_queue(code))     # get broker queue

# stop async data receive
quote_ctx.stop()

# close the object
quote_ctx.close()

# create the stock trade object
# trade_hk_ctx = ft.OpenHKTradeContext(host="127.0.0.1", port=11111)

# trade interface list
# print(trade_hk_ctx.unlock_trade(password='123456'))                # unlock the trade interface
# print(trade_hk_ctx.accinfo_query(trd_env=ft.TrdEnv.SIMULATE))      # check the account info
# print(trade_hk_ctx.place_order(price=1.1,
#                                qty=2000,
#                                code=code,
#                                trd_side=ft.TrdSide.BUY,
#                                order_type=ft.OrderType.NORMAL,
#                                trd_env=ft.TrdEnv.SIMULATE))  # create the order
# print(trade_hk_ctx.order_list_query(trd_env=ft.TrdEnv.SIMULATE))      # check the order list
# print(trade_hk_ctx.position_list_query(trd_env=ft.TrdEnv.SIMULATE))    # check the position list

# trade_hk_ctx.close()