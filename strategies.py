
import time

from helpers import *
from bot import *

# BOND
'''
Scalp buy when someone wants to sell for less than 1000
Scalp sell when someone wants to buy for more than 1000
'''
def bond(exchange) :
    data = read_from_exchange(exchange)

    # print(data)
    if data['type'] == 'book' and data['symbol'] == 'BOND':
        current_bids, current_asks = data['buy'], data['sell']
        
        # print('current bids', current_bids)
        # print('current_asks', current_asks)

        for ask_price, ask_size in current_asks:

            buy_order1 = create_buy_sell_order(int(time.time()), 'BOND', 'BUY', 999, 100)
            write_to_exchange(exchange, buy_order1)

            # buy_order2 = create_buy_sell_order(int(time.time()), 'BOND', 'BUY', 998, 25)
            # write_to_exchange(exchange, buy_order2)

        for bid_price, bid_size in current_bids:

            sell_order1 = create_buy_sell_order(int(time.time()), 'BOND', 'SELL', 1001, 100)
            write_to_exchange(exchange, sell_order1)
            
            # sell_order2 = create_buy_sell_order(int(time.time()), 'BOND', 'SELL', 1002, 25)
            # write_to_exchange(exchange, sell_order2)


def mean(list):
    return sum(list)//len(list)

stock_price_history = []
adr_price_history = []

def arbitrage(exchange):
    
    data = read_from_exchange(exchange)

    if data['type'] == 'trade':
        if (data['symbol'] == 'VALBZ'):
            stock_price_history.append(data['price'])
        if (data['symbol'] == 'VALE'):
            adr_price_history.append(data['price'])    

    atr(exchange, stock_price_history[-50:], adr_price_history[-50:])


def atr(exchange, stock_price_history, adr_price_history):
    if (len(stock_price_history) != 0 and len(adr_price_history) != 0):
        stock_price_history_mean = mean(stock_price_history)
        adr_price_history_mean = mean(adr_price_history)

        # print("stock history", stock_price_history)
        # print("etf history", adr_price_history)
        if (stock_price_history_mean - adr_price_history_mean >= 2):
            buy_order = create_buy_sell_order(int(time.time()), 'VALE', 'BUY', stock_price_history_mean - 1, 1)
            write_to_exchange(exchange, buy_order)

            # convert_order = create_convert_order(int(time.time()), 'VALE', 'SELL', 1)
            # write_to_exchange(exchange, convert_order)

            sell_order = create_buy_sell_order(int(time.time()), 'VALE', 'SELL', stock_price_history_mean + 1, 1)
            write_to_exchange(exchange, sell_order)
        # return [True, stock_price_history_mean, adr_price_history_mean]

gs_history = []
ms_history = []
wfc_history = []
xlf_history = []

def etf_arb(exchange):
    data = read_from_exchange(exchange)

    if data['type'] == 'trade':
        if (data['symbol'] == 'GS'):
            gs_history.append(data['price'])    
        if (data['symbol'] == 'MS'):
            ms_history.append(data['price'])
        if (data['symbol'] == 'WFC'):
            wfc_history.append(data['price'])    
        if (data['symbol'] == 'XLF'):
            xlf_history.append(data['price'])    

    etf(exchange, gs_history[-1000:], ms_history[-1000:], wfc_history[-1000:], xlf_history[-1000:])

def etf(exchange, gs, ms, wfc, xlf):
    if (len(gs) != 0 and len(ms) != 0 and len(wfc) != 0 and len(xlf) != 0):
        gs_mean = mean(gs)
        ms_mean = mean(ms)
        wfc_mean = mean(wfc)
        xlf_mean = mean(xlf)

        approximate_price = (3000 + 2*gs_mean + 3*ms_mean + 2*wfc_mean)//10
        
        if approximate_price - xlf_mean > 150:
            buy_order1 = create_buy_sell_order(int(time.time()), 'XLF', 'BUY', xlf_mean - 1, 100)
            write_to_exchange(exchange, buy_order1)

            convert_order = create_convert_order(int(time.time()), 'XLF', 'SELL', 100)
            write_to_exchange(exchange, convert_order)

            buy_order2 = create_buy_sell_order(int(time.time()), 'BOND', 'SELL', 999, 30)
            write_to_exchange(exchange, buy_order2)

            buy_order3 = create_buy_sell_order(int(time.time()), 'GS', 'SELL', gs_mean - 1, 20)
            write_to_exchange(exchange, buy_order3)

            buy_order4 = create_buy_sell_order(int(time.time()), 'MS', 'SELL', ms_mean - 1, 30)
            write_to_exchange(exchange, buy_order4)

            buy_order5 = create_buy_sell_order(int(time.time()), 'WFC', 'SELL', wfc_mean - 1, 20)
            write_to_exchange(exchange, buy_order5)

            # buy_order = create_buy_sell_order(int(time.time()), 'XLF', 'BUY', approximate_price - 1, 1)
            # write_to_exchange(exchange, buy_order)

            # sell_order = create_buy_sell_order(int(time.time()), 'XLF', 'SELL', approximate_price + 1, 1)
            # write_to_exchange(exchange, sell_order)
        else:
            buy_order1 = create_buy_sell_order(int(time.time()), 'BOND', 'BUY', 999, 30)
            write_to_exchange(exchange, buy_order1)

            buy_order2 = create_buy_sell_order(int(time.time()), 'GS', 'BUY', gs_mean - 1, 20)
            write_to_exchange(exchange, buy_order2)

            buy_order3 = create_buy_sell_order(int(time.time()), 'MS', 'BUY', ms_mean - 1, 30)
            write_to_exchange(exchange, buy_order3)

            buy_order4 = create_buy_sell_order(int(time.time()), 'WFC', 'BUY', wfc_mean - 1, 20)
            write_to_exchange(exchange, buy_order4)

            convert_order = create_convert_order(int(time.time()), 'XLF', 'BUY', 100)
            write_to_exchange(exchange, convert_order)

            buy_order5 = create_buy_sell_order(int(time.time()), 'XLF', 'SELL', xlf_mean + 1, 100)
            write_to_exchange(exchange, buy_order5)

