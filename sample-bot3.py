#!/usr/bin/python

# ~~~~~==============   HOW TO RUN   ==============~~~~~
# 1) Configure things in CONFIGURATION section
# 2) Change permissions: chmod +x bot.py
# 3) Run in loop: while true ; do ./sample-bot2.py ; sleep 1; done

from __future__ import print_function

import sys
import socket
import json
import time
import random

# ~~~~~============== CONFIGURATION  ==============~~~~~
# replace REPLACEME with your team name!
team_name="DARINA"
# This variable dictates whether or not the bot is connecting to the prod
# or test exchange. Be careful with this switch!
test_mode = True

# This setting changes which test exchange is connected to.
# 0 is prod-like
# 1 is slower
# 2 is empty
test_exchange_index=0
prod_exchange_hostname="production"

port=25000 + (test_exchange_index if test_mode else 0)
exchange_hostname = "test-exch-" + team_name if test_mode else prod_exchange_hostname

# ~~~~~============== NETWORKING CODE ==============~~~~~
def connect():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((exchange_hostname, port))
    return s.makefile('rw', 1)

def write_to_exchange(exchange, obj):
    json.dump(obj, exchange)
    exchange.write("\n")

def read_from_exchange(exchange):
    return json.loads(exchange.readline())

# ~~~~~============== CODE ==============~~~~~

def trade_bonds(exchange, order_id):
    write_to_exchange(exchange, {"type": "add", "order_id": order_id, "symbol":"BOND", "dir": "BUY", "price": 999, "size": 10 })
    #time.sleep(.01)
    order_id += 1
    write_to_exchange(exchange, {"type": "add", "order_id": order_id, "symbol":"BOND", "dir": "SELL", "price": 1001, "size": 10 })
    #time.sleep(.01)

def sell_bonds(exchange, order_id):
       write_to_exchange(exchange, {"type": "add", "order_id": order_id, "symbol":"BOND", "dir": "SELL", "price": 1001, "size": 10 })
       order_id += 1
       #time.sleep(.01)

def buy_bonds(exchange, order_id):
       write_to_exchange(exchange, {"type": "add", "order_id": order_id, "symbol":"BOND", "dir": "BUY", "price": 999, "size": 10 })
       order_id += 1
       #time.sleep(.01)


# ~~~~~============== MAIN LOOP ==============~~~~~

def main():
    print("RESTART")
    exchange = connect()
    write_to_exchange(exchange, {"type": "hello", "team": team_name.upper()})
    hello_from_exchange = read_from_exchange(exchange)
    # A common mistake people make is to call write_to_exchange() > 1
    # time for every read_from_exchange() response.
    # Since many write messages generate marketdata, this will cause an
    # exponential explosion in pending messages. Please, don't do that!
    print("The exchange replied:", hello_from_exchange, file=sys.stderr)
    # -------------------------------------------------------------------

    order_id = 0
    INITIAL_PRICE = 1000
    DIR_SELL = 'sell'
    DIR_BUY = 'buy'

    # b = 0
    # s = 0
    # t = 0

    while True:
        res = read_from_exchange(exchange)

        #print(res)

        if DIR_SELL in res:
            # print(res)
            # print(res[DIR_SELL])
            # print('-----', res[DIR_SELL][0])
            if len(res[DIR_SELL]) > 0 and res[DIR_SELL][0][0] > INITIAL_PRICE:
                #print('Buying...')
                #b += 1
                buy_bonds(exchange, order_id)
                order_id += 1

        if DIR_BUY in res:
            if len(res[DIR_BUY]) > 0 and res[DIR_BUY][0][0] < INITIAL_PRICE:
                #print('Selling...')
                #s += 1
                sell_bonds(exchange, order_id)
                order_id += 1

        elif random.random() < 0.5:
            #print('Trading...')
            #t += 1
            trade_bonds(exchange, order_id)
            order_id += 2

        # print('STATS:')
        # print('b', b)
        # print('s', s)
        # print('t', t)
        
     

if __name__ == "__main__":
    main()