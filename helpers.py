import json

def create_buy_sell_order(order_id, symbol, dir, price, size) :
    return {
        "type" : "add",
        "order_id" : order_id,
        "symbol" : symbol,
        "dir" : dir,
        "price" : price,
        "size" : size
    }

def create_cancel_order(order_id) :
    return {
        "type" : "cancel",
        "order_id" : order_id
    }

def create_convert_order(order_id, symbol, dir, size) :
    return {
        "type" : "convert",
        "order_id" : order_id,
        "symbol" : symbol,
        "dir" : dir,
        "size" : size
    }